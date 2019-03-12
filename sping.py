#!/usr/bin/env python3

import subprocess
import platform
import os
import sys
from time import sleep

operating_sys = platform.system()

if len(sys.argv) > 1:
	nas = sys.argv[1]
else:
	print("Enter the address. for example sping 127.0.0.1")
	sys.exit(1)

def ping(ip):
	ok = 0
	nok = 0

	if operating_sys == 'Windows':
		ping_command = ['ping', ip, '-n 1']
		shell_needed = True
	else:
		ping_command = ['ping', ip, '-c 1']
		shell_needed = False

	ping_output = subprocess.run(ping_command, shell=shell_needed, stdout=subprocess.PIPE)
	success = ping_output.returncode

	if success == 0:
		if operating_sys == 'Windows':
			print('Host %s is alive!' % ip)
		else:
			out = ping_output.stdout.decode("utf-8").split()
			time = out[13].split('=')
			print('Host %s is alive time=%s %s!' % (ip, time[1], out[14]))
			os.system('play -nq -t alsa synth 0.2 sine 800')
	else:
		if operating_sys == 'Windows':
			print('Host %s is dead!' % ip)
		else:
			print('Host %s is dead!' % ip)
			os.system('play -nq -t alsa synth 0.5 sine 200')

while 1:
	try:
		ping(nas)
		sleep(1)
	except (KeyboardInterrupt, SystemExit):
		print("Bye!")
		break
