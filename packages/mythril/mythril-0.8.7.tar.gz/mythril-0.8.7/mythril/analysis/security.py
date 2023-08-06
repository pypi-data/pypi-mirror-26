from mythril.analysis.report import Report
from .modules import delegatecall_forward, unchecked_suicide, ether_send, unchecked_retval


def fire_lasers(statespace):

	issues = []

	issues += delegatecall_forward.execute(statespace)
	issues += unchecked_suicide.execute(statespace)
	issues += ether_send.execute(statespace)

	# still needs some work
	# issues += unchecked_retval.execute(statespace)

	if (len(issues)):
		report = Report(issues)
		print(report.as_text())
