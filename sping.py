#!/usr/bin/env python3

import subprocess
import platform
import os
import sys
import re
from time import sleep

def read_out(out):
	string = out.decode("utf-8").split()

	if len(string) == 36:
		duration = string[14]
		ei = string[15]
	else:
		duration = string[13]
		ei = string[14]

	duration = duration.split('=')

	return [float(duration[1]), ei]

def ping(ip, stats):
	if operating_sys == 'Windows':
		ping_command = ['ping', ip, '-n 1']
		shell_needed = True
	else:
		ping_command = ['ping', ip, '-c 1']
		shell_needed = False

	ping_output = subprocess.run(ping_command, shell=shell_needed, stdout=subprocess.PIPE)
	success = ping_output.returncode

	stats[0] += 1

	if success == 0:
		if operating_sys == 'Windows':
			print('Host %s is alive!' % ip)
		else:
			time = read_out(ping_output.stdout)
			print('Host %s is alive time=%s %s' % (ip, time[0], time[1]))
			if beep == 1 or beep == 0:
				os.system('play -nq -t alsa synth 0.2 sine 800')
		stats[1] += 1
		stats[2].append(time[0])
	else:
		if operating_sys == 'Windows':
			print('Host %s is dead!' % ip)
		else:
			print('Host %s is dead!' % ip)
			if beep == 2 or beep == 0:
				os.system('play -nq -t alsa synth 0.5 sine 200')

	return stats

def avg(lst):
	return round((sum(lst) / len(lst)), 3)

beep = 0
host = ""
if len(sys.argv) > 1:

	for opt in sys.argv:
		if opt == "-h":
			print("Usage: sping [-f|s] host")
			print("	-s - sound only successful packages")
			print("	-f - sound only failed packages")
			print("	-v - print version")
			print("	-h - print this message")
			sys.exit(0)
		elif opt == "-s":
			beep = 1
		elif opt == "-f":
			beep = 2
		elif opt == "-v":
			print("Version: 1.0")
			sys.exit(0)
		elif re.match(r'^[^-=+*/\\%$#@]\w{0,}', opt) and opt != sys.argv[0]:
			host = opt

else:
	print("Usage: sping [-f|s] host")
	sys.exit(1)

if host == "":
	print("Usage: sping [-f|s] host")
	sys.exit(1)

operating_sys = platform.system()
result = [0, 0, []]

while 1:
	try:
		result = ping(host, result)
		sleep(1)
	except (KeyboardInterrupt, SystemExit):
		loss = result[0] - result[1]
		per_loss = loss * 100 / result[0]
		print("--- %s ping statistics ---" % host)
		print("{} packets transmitted, {} received,  packet loss {}%".format(result[0], result[1], round(per_loss)))
		if len(result[2]) > 1:
			print("rtt min/avg/max = {}/{}/{} ms".format(min(result[2]), avg(result[2]), max(result[2])))
		break