#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2015 Demo User <debian@beaglebone>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""Serial port to IMEON.
This module handles low level communication with the Serial port of IMEON
"""
import sys
import serial
import time
import os

class TTYDevice(object):
	    
	def __init__(self, port):
        ###Low level Serial (TTY) port access via serial library.

        ###:param port: the Serial port name, for example /dev/ttyUSB0.

        ###:type port: string
		
		#Connect the serial port to BBB
		os.popen("modprobe usbserial vendor=0x067b product=0x2303").read()
		os.popen("dmesg | grep ttyUSB0").read()
		#open serial port
		self.ser = serial.Serial(
					port=port,
					baudrate=2400,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
					bytesize=serial.EIGHTBITS
				)
				
		if not self.ser:
			raise IOError("IMEON not found")
		
		self.ser.flushInput() #flush input buffer, discarding all its contents
		self.ser.flushOutput()#flush output buffer, aborting current output 
			                 #and discard all that is in buffer	
	
	def read_datas(self,size):
        ###Receive serial data from IMEON.

        ###If the read fails for any reason, an :obj:IOError exception
        ###is raised.
		
        ###:param size: the number of bytes to read.

        ###:type size: int

        ###:return: the data received.

        ###:type return: list sting

		result = self.ser.read(size)
		if not result or len(result) < size:
			raise IOError('read_data serial failed')
		return str(result)

	def write_datas(self, buf):
        ###Send data to IMEON.

        ###If the write fails for any reason, an :obj:IOError exception
		###is raised.

        ###:param buf: the data to send.

        ###:type buf: ASCII

        ###:return: success status.

        ###:rtype: bool
  
		result = self.ser.write(buf)
		if result != len(buf):
			raise IOError('write_data serial failed')
		return True
	
	def loops_wr(self, buf, size, timen, times):
		###Receive data from IMEON in a certain time.

        ###If the read fails for any reason, an :obj:IOError exception
        ###is raised.
        
        ###:param buf: the data to send.

        ###:type buf: ASCII

        ###:param size: the number of bytes to read.

        ###:type size: int
        
        ###:param timen: recieve data in time seconds.

        ###:type timen: int (in seconds)
        
        ###:param times: recieve data every times seconds.

        ###:type times: int (in seconds)

        ###:return: the data received.

        ###:rtype: list in string
        
		#second = 0
		
		test = 0
		datas=[]
		timeout = time.time() + timen   # time seconds from now	    
		while True:
			#Sometimes there are information in the serial bus that is not necessary
			if 	self.ser.inWaiting() > 0:
				self.read_datas(self.ser.inWaiting())
			#write data
			self.write_datas(buf)
			#give somme time to seral port
			time.sleep(1)
			#read data
			dat=self.read_datas(size)
			#Save datas in a list
			datas.append(dat[1:])
			#read datas in times seconds
			time.sleep(times-1)
			if test == 5 or time.time() > timeout:
				break
			test = test - 1
		self.ser.close()
		return datas
