#! /usr/bin/env python

import argparse
import os
import signal
import subprocess

def execmd(command, timeout=30):
	"""
	Executes the specified command on command line and returns (or reports) results.

	Parameters:
		command (string or tuple): describes a command and its arguments.
		timeout (int): (optional (default is 30 seconds)) timeout (in seconds) describes when to kill the command and report it timed out.

	Returns:
		dictionary: returning results of return code, stdout, stderr, and boolean describing if the command timed out or not.
	"""
	cmd_timed_out = False
	stdout = stderr = ""
	returncode = 1
	try:
		proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = proc.communicate(timeout=timeout)
		returncode = proc.returncode
		stdout, stderr = stdout.decode("utf-8"), stderr.decode("utf-8")
	except Exception as e:
		if isinstance(e, subprocess.TimeoutExpired):
			os.kill(proc.pid, signal.SIGTERM)
			cmd_timed_out = True
		else:
			raise e
	return {"returncode":returncode, "stdout":stdout, "stderr":stderr, "timedout":cmd_timed_out}

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='This script executes the specified command and reports results')
	parser.add_argument("-to", "--timeout", default=30, help="Specify amount of time in seconds to kill command if it doesn't return in time.")
	parser.add_argument("-s", "--silent", action='store_true', default=False, help="Specify suppressing command output or not.")
	parser.add_argument("-c", "--command", nargs='+', help="Specify the command and its arguments to execute and report on.")
	args = parser.parse_args()
	cmd = tuple(args.command)
	results = execmd(cmd, int(args.timeout))
	if (not bool(args.silent)):
		print(f"""
	Command Results:

	Command: '{cmd}'

	Return Code: {results["returncode"]}

	Timedout: {results["timedout"]}

	STDOUT: 
	'''
	{results["stdout"]}
	'''

	STDERR: 
	'''
	{results["stderr"]}
	'''
	""")
