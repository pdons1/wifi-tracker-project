#!/usr/bin/python

import threading
import argparse
import sys
import time
import subprocess
import manuf
import datetime as dt

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
conf.verb = 0

from logging.handlers import RotatingFileHandler
import collections
import requests
import base64
import json
import re
from os import system, path, getuid, uname
from numpy.random import permutation

whmp = manuf.MacParser()

DESCRIPTIONTXT = "test of description"
NAME = 'TESTING'

#this parses the command line for any provided arguments
def parse_args():
	parser = argparse.ArgumentParser(description=DESCRIPTIONTXT)
	parser.add_argument('-i', '--interface', help="capture interface")
	parser.add_argument('-w', '--waittime', help="time to wait in between switching channels")
	return parser.parse_args()

#get mac address
def getMac(interface_in):
	mac_address = open('/sys/class/net/%s/address' % interface_in).read().rstrip()
	return mac_address
	
#get the list of channels available
def getChannelList(interface_in):
	channelNumList = []
	command = ["iwlist", interface_in, "channel"]
	
	process = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	process.wait()
	
	#save the output (list of channels)
	(stdoutput, stderrdata) = process.communicate()
	#split the lines at each \n character
	stdoutput = stdoutput.splitlines()
	
	#clean up list, first element not needed and last 2 not needed
	stdoutput.pop()
	stdoutput.pop()
	stdoutput.pop(0)
	#add channel numbers to channeNumList
	for line in stdoutput:
		#decode line from class<bytes> to a string, subprocess does some weird thing that shows outputs as a byte class
		#after decoding, split the line to make a list of the words
		word_list = (line.decode()).split()
		#the channel number is located at index 1
		channelNumber = int(word_list[1])
		channelNumList.append(channelNumber)
	return channelNumList


def get_rssi(extra):
	rssi = int(-(256 - ord(extra[-2:-1])));
	if rssi not in xrange(-100, 0):
		rssi = (-(256 - ord(extra[-4:-3])));
	if rssi < -100:
		return -1;
	return rssi;
	
def packetHandler(pkt):
	#if it's a WiFi packet, print it out
	if pkt.haslayer(Dot11):
		ts = time.time()
		st = dt.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		
		#rssi_val = str(get_rssi(pkt.notdecoded))
		print(st, pkt.addr2)
	
def main(interface_in, time_in):
	#try:
	sniff(iface = interface_in, prn = packetHandler, store = 0, timeout = time_in)
	#except Exception as e:
	#	print('Exception has been caught while running sniff()', e)
	
def error_checking(args):
	global interface, output_file, WAIT_TIME

	#check if an interface has been provided
	if not args.interface:
		print("interface has not been provided.  Please run again with -i [INTERFACE] or --interface [INTERFACE]")
		exit(0)
	else:
		interface = args.interface
		
	#check to see if a time to wait in between hopping channels has been provided
	if not args.waittime:
		WAIT_TIME = 0.25
	else:
		WAIT_TIME = float(args.waittime)

def set_monitor_mode(interface_in):
	#set device to monitor mode, we removed the monitor mode check (ADD THIS LATER)
	print('Setting to monitor mode...')
	command = ['airmon-ng', 'start', interface_in]
	process = subprocess.Popen(command)
	process.wait()
	if 'mon' not in interface_in:
		interface_in = interface_in + 'mon'
	return interface_in
		


if __name__=="__main__":
	args = parse_args()
	error_checking(args)
	interface = set_monitor_mode(interface)
	
	#keep running until ctrl + c
	try:
		#sniff(iface = interface, prn = packetHandler, store = 0)
		#channel hopping
		while True:
			for channel_num in permutation(getChannelList(interface)):
				command = ['iw', 'dev', interface, 'set', 'channel', str(channel_num)]
				process = subprocess.Popen(command)			
				process.wait()
				
				print("sniffing on channel", channel_num) 
					
				try:
					main(interface, WAIT_TIME)
				except KeyboardInterrupt:
					break
					
	except KeyboardInterrupt:
		pass
		
	# Turn off monitor mode
	command = ['airmon-ng', 'stop', interface]
	end_command = subprocess.Popen(command)
	end_command.wait()
	
	
	

