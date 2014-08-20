#!/usr/bin/python

'''
Author: 
	Proteas
Date:
	2014-08-20
Purpose:
	connect idevice
Usage:
	add the following line to ~/.lldbinit
	command script import ~/.lldb/idevice_connect.py
'''

import lldb
import commands
import shlex
import optparse
import re

def __lldb_init_module (debugger, dict):
	debugger.HandleCommand('command script add -f idevice_connect.idevice_connect idevice_connect')
	print 'The "idevice_connect" command has been installed'

def idevice_connect(debugger, command, result, dict):
	lldb.debugger.HandleCommand ('platform select remote-ios')
	lldb.debugger.HandleCommand ('process connect connect://127.0.0.1:11022')