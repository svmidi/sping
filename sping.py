#!/usr/bin/env python3

import subprocess
import platform
import os
import sys
from time import sleep

operating_sys = platform.system()

if len(sys.argv) > 1:
	host = sys.argv[1]
else:
	print("Enter the address. for example sping 127.0.0.1")
	sys.exit(1)

def read_out(out):
	string = out.decode("utf-8").split()

	if len(string) == 36:
		duration = string[14]
		ei = string[15]
	else:
		duration = string[13]
		ei = string[14]

	duration = duration.split('=')

	return [duration[1], ei]

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
			os.system('play -nq -t alsa synth 0.2 sine 800')
		stats[1] += 1
	else:
		if operating_sys == 'Windows':
			print('Host %s is dead!' % ip)
		else:
			print('Host %s is dead!' % ip)
			os.system('play -nq -t alsa synth 0.5 sine 200')

	return stats

result = [0, 0]

while 1:
	try:
		result = ping(host, result)
		sleep(1)
	except (KeyboardInterrupt, SystemExit):
		loss = result[0] - result[1]
		per_loss = loss * 100 / result[0]
		print("--- %s ping statistics ---" % host)
		print("{} packets transmitted, {} received,  packet loss {}%".format(result[0], result[1], round(per_loss)))
		break