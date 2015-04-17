#!/usr/bin/python

'''
Author: 
	Proteas
Date:
	2015-04-17
Purpose:
	set breakpoint on address, auto calcute slide
Usage:
	add the following line to ~/.lldbinit
	command script import ~/.lldb/bk_addr.py
'''

import lldb
import commands
import shlex
import optparse
import re

def __lldb_init_module (debugger, dict):
	debugger.HandleCommand('command script add -f bk_addr.bk_addr bk_addr')
	print 'The "bk_addr" command has been installed, usage: bk_addr 0x00000001'

def create_command_arguments(command):
	return shlex.split(command)

def bk_addr(debugger, command, result, dict):

	# common objects
	target = debugger.GetSelectedTarget()
	process = target.GetProcess()
	thread = process.GetSelectedThread()
	frame = thread.GetSelectedFrame()

	# parse command params
	args = create_command_arguments(command)
	if len(args) != 1:
		print "[bk_addr]: invalid param"
		return

	# find text section
	target_module = target.GetModuleAtIndex(0)
	text_section = None
	for sec in target_module.section_iter():
		if sec.GetName() == '__TEXT':
			text_section = sec
	
	if not text_section:
		print "bk_addr]: can't find __TEXT"
		return

	# calcute slide
	slide = text_section.GetLoadAddress(target) - text_section.GetFileAddress()
	print "[bk_addr]: module slide is: %#x" % slide

	# get file address
	target_file_address = long(args[0], 0)
	# calcute load address
	target_load_address = target_file_address + slide

	# set breakpoint on address
	target.BreakpointCreateByAddress(target_load_address)
