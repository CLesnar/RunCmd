#! /usr/bin/env python

__version__ = '0.1.0'
__all__ = [
    'execmd',
]

import argparse
import os
import signal
import subprocess

def execmd(command, timeout=60):
	"""
	Executes the specified command on command line and reports results.

	Parameters:
		command (string or tuple): describes a command and its arguments.
		timeout (int): (optional (default is 30 seconds)) timeout (in seconds) describes when to kill the command and report it timed out.

	Returns:
		dictionary: returning results of return code, stdout, stderr, and boolean describing if the command timed out or not.
	"""
	results = {"returncode":1, "stdout":"", "stderr":"", "timedout":False}
	try:
		proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = proc.communicate(timeout=timeout)
		results["returncode"], results["stdout"], results["stderr"] = proc.returncode, stdout.decode("utf-8"), stderr.decode("utf-8")
	except Exception as e:
		if isinstance(e, subprocess.TimeoutExpired):
			os.kill(proc.pid, signal.SIGTERM)
			results["timedout"] = True
		else:
			raise e
	return results

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='This script executes the specified command and reports results')
	parser.add_argument("-t", "--timeout", default=30, help="Specify amount of time in seconds to kill command if it doesn't return in time.")
	parser.add_argument("-s", "--silent", default=False, help="Specify suppressing command output or not.")
	parser.add_argument("-c", "--command", nargs='+', help="Specify the command and its arguments to execute and report on.")
	args = parser.parse_args()
	cmd = tuple(args.command)
	cmd_str = " ".join(args.command)
	results = execmd(cmd_str, int(args.timeout))
	if (not bool(args.silent)):
		print(f"""
Command: '{cmd_str}'
Return Code: {results["returncode"]}
Timedout: {results["timedout"]}
Output: 
{results["stdout"]}
{results["stderr"]}""")
