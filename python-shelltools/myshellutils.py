import os
import sys

def get_cmd_stdout(cmd):
	with os.popen(cmd) as f:
		return f.read()

def cmd(cmd, check=True):
	ret = os.system(cmd)
	if check and ret != 0:
		raise Exception('Command Exec Error')

def write_stdout(s):
	sys.stdout.write(s)

def kvfile_item_value_get(file, key):
	with open(file) as f:
		lines = f.readlines()

		for line in lines:
			if line.startswith(key + '='):
				val = line.split('=')[1].strip()
				return val

	raise Exception('Key Not Found')

def kvfile_item_value_set(file, key, val):
	mark = False
	with open(file, mode='r') as f:
		lines = f.readlines()
		for i in range(len(lines)):
			if lines[i].startswith(key + '='):
				lines[i] = key + '=' + val + '\n'
				mark = True

	if mark is False:
		raise Exception('Key Not Found')

	with open(file, mode='w') as f:
		for line in lines:
			f.write(line)
