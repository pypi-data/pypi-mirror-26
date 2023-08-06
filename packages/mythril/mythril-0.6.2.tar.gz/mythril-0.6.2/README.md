# Mythril

<img height="60px" align="right" src="/static/mythril.png"/>

Mythril is a reverse engineering and bug hunting framework for the Ethereum blockchain.

  * [Installation and setup](#installation-and-setup)
  * [Command line usage](#command-line-usage)
    + [Input formats](#input-formats)
      - [Working with on-chain contracts](#working-with-on-chain-contracts)
      - [Working with Solidity files](#working-with-solidity-files)
    + [Disassembler](#disassembler)
    + [Control flow graph](#control-flow-graph)
    + [Contract search](#contract-search)
      - [Searching from the command line](#searching-from-the-command-line)
      - [Finding cross-references](#finding-cross-references)

## Installation and setup

Install from Pypi:

```bash
$ pip install mythril
```

Or, clone the GitHub repo to install the newest master branch:

```bash
$ git clone https://github.com/b-mueller/mythril/
$ cd mythril
$ python setup.py install
```

Note that Mythril requires Python 3.5 to work.

## Command line usage

The Mythril command line tool (aptly named `myth`) allows you to conveniently access most of Mythril's functionality.

### Input formats

Mythril can handle various sources and input formats, including bytecode, addresses of contracts on the blockchain, and Solidity source code files.

#### Working with on-chain contracts

To pull contracts from the blockchain you need an Ethereum node that is synced with the network. By default, Mythril will query a local node via RPC. Alternatively, you can connect to a remote service such as [INFURA](https://infura.io):

```
$ myth --rpchost=mainnet.infura.io/{API-KEY} --rpcport=443  --rpctls=True (... etc ...)
```

The recommended way is to use [go-ethereum](https://github.com/ethereum/go-ethereum). Start your local node as follows:

```bash
$ geth --rpc --rpcapi eth,debug --syncmode fast
```

#### Working with Solidity files

In order to work with Solidity source code files, the [`solc` command line compiler](http://solidity.readthedocs.io/en/develop/using-the-compiler.html) needs to be installed and in path. You can then provide the source file(s) as positional arguments, e.g.:

```bash
$ myth -g ./graph.html myContract.sol
```

### Disassembler

Use the `-d` flag to disassemble code. The disassembler accepts a bytecode string or a contract address as its input.

```bash
$ myth -d -c "0x6060"
0 PUSH1 0x60
```

Specifying an address via `-a ADDRESS` will download the contract code from your node. Mythril will try to resolve function names using the signatures in `database/signature.json`:

```bash
$ myth -d -a "0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208"
0 PUSH1 0x60
2 PUSH1 0x40
4 MSTORE
(...)
1135 - FUNCTION safeAdd(uint256,uint256) -
1136 CALLVALUE
1137 ISZERO
```

### Control flow graph

Mythril integrates the LASER symbolic virtual machine. Right now, this is mainly used for CFG generation. The `-g FILENAME` option generates an [interactive jsViz graph](http://htmlpreview.github.io/?https://github.com/b-mueller/mythril/blob/master/static/mythril.html):

```bash
$ myth -g ./graph.html -a "0xFa52274DD61E1643d2205169732f29114BC240b3"
```

![callgraph](https://raw.githubusercontent.com/b-mueller/mythril/master/static/callgraph7.png "Call graph")

~~The "bounce" effect, while awesome (and thus enabled by default), sometimes messes up the graph layout.~~ Try adding the `--enable-physics` flag for a very entertaining "bounce" effect that unfortunately completely destroys usability.

### Contract search

Mythril builds its own contract database to enable fast search operations. This is to enable operations like those described in the [legendary "Mitch Brenner" blog post](https://medium.com/@rtaylor30/how-i-snatched-your-153-037-eth-after-a-bad-tinder-date-d1d84422a50b) in ~~seconds~~ minutes instead of days. Unfortunately, the initial sync process is slow. You don't need to sync the whole blockchain right away though: If you abort the syncing process with `ctrl+c`, it will be auto-resumed the next time you run the `--init-db` command.

```bash
$ myth --init-db
Starting synchronization from latest block: 4323706
Processing block 4323000, 3 individual contracts in database
(...)
```

The default behavior is to only sync contracts with a non-zero balance. You can disable this behavior with the `--sync-all` flag, but be aware that this will result in a huge (as in: dozens of GB) database.

#### Searching from the command line

The search feature allows you to find contract instances that contain specific function calls and opcode sequences. It supports simple boolean expressions, such as:

```bash
$ myth --search "func#changeMultisig(address)#"
$ myth --search "code#PUSH1 0x50,POP#"
$ myth --search "func#changeMultisig(address)# and code#PUSH1 0x50#"
```

#### Finding cross-references

It is often useful to find other contracts referenced by a particular contract. E.g.:

```bash
$ myth --search "code#DELEGATECALL#"
Matched contract with code hash 07459966443977122e639cbf7804c446
Address: 0x76799f77587738bfeef09452df215b63d2cfb08a, balance: 1000000000000000
$ myth --xrefs -a 0x76799f77587738bfeef09452df215b63d2cfb08a
5b9e8728e316bbeb692d22daaab74f6cbf2c4691
```

## Credit

- JSON RPC library is adapted from [ethjsonrpc](https://github.com/ConsenSys/ethjsonrpc) (it doesn't seem to be maintained anymore, and I needed to make some changes to it).

- The signature data in `signatures.json` has been obtained from the [Ethereum Function Signature Database](https://www.4byte.directory).

## Disclaimer: Act responsibly!

The purpose of project is to aid discovery of vulnerable smart contracts on the Ethereum mainnet and support research for novel security flaws. If you do find an exploitable issue or vulnerable contract instances, please [do the right thing](https://en.wikipedia.org/wiki/Responsible_disclosure). Also, note that vulnerability branding ("etherbleed", "chainshock",...) is highly discouraged as it will annoy the author and others in the security community.
