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

"""USB port to IMEON, using PyUSB v1.0.
This module handles low level communication with the USB port of IMEON
via the `PyUSB <http://sourceforge.net/apps/trac/pyusb/>`_ library
(version 1.0). """

import sys
import usb.core
import usb.util
import time

class USBDevice(object):
	def __init__(self, idVendor, idProduct):
        ###Low level USB port access via PyUSB 1.0 library

        ###:param idVendor: the USB vendor ID number for example 0x1941

        ###:type idVendor: int

        ###:param idProduct: the USB product ID number for example 0x8021

        ###:type idProduct: int
        
		self.dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)
		if not self.dev:
			raise IOError("IMEON not found")
		if sys.platform.startswith('linux'):
			try:
				detach = self.dev.is_kernel_driver_active(0)
			except NotImplementedError:
				detach = True
			if detach:
				try:
					self.dev.detach_kernel_driver(0)
				except usb.core.USBError:
					pass
        #self.dev.reset()
		self.dev.set_configuration()
		usb.util.claim_interface(self.dev, 0)

	def endpoint_dev(self):
		'''Get the Endpoint of USB port.'''
		
		endpoint = self.dev[0][(0,0)][0]
		return endpoint
		
	def read_datap(self,bEndpointAdress,size):
        ###Receive data from IMEON.

        ###If the read fails for any reason, an :obj:IOError exception
        ###is raised.
		
		###:param bEndpointAdress: Read adress of the USB port
		
		###:type bEndpointAdress: Hex

        ###:param size: the number of bytes to read.

        ###:type size: int

        ###:return: the data received.

        ###:rtype: int

		result = self.dev.read(bEndpointAdress, size, timeout=0)
		if not result or len(result) < size:
			raise IOError('read_data USB failed')
		return result

	def write_datap(self, buf):
        ###Send data to IMEON.

        ###:If the write fails for any reason, an :obj:IOError exception
        ###:is raised.

        ###:param buf: the data to send.

        ###:type buf: ASCII

        ###:return: success status.

        ###:rtype: bool

		bmRequestType = usb.util.build_request_type(
			usb.util.ENDPOINT_OUT,
			usb.util.CTRL_TYPE_CLASS,
			usb.util.CTRL_RECIPIENT_INTERFACE
			)
		result = self.dev.ctrl_transfer(
			bmRequestType=bmRequestType,
			bRequest=usb.REQ_SET_CONFIGURATION,
 			data_or_wLength=buf,
			wValue=0,
			timeout=0)
		if result != len(buf):
			raise IOError('write_data USB failed')
		return True
	
	def loop_read(self, bEndpointAdress, sizeword, size, n):
		###Receive data from IMEON, n times.

        ###If the read fails for any reason, an :obj:`IOError` exception
        ###is raised.
		
		###:param bEndpointAdress: Read adress of the USB port
		
		###:type bEndpointAdress: Hex

        ###:param sizeword: the max number of bytes that the port can read.

        ###:type sizeword: int
        
        ###:param size: the total number of bytes to read.

        ###:type size: int
        
        ###:param n: the number of times for the loop.

        ###:type n: int

        ###:return: the data received.

        ###:rtype: int
        
		bites=[]
		i=0
		while i < n:
			bites+=self.read_datap(bEndpointAdress,sizeword)
			i+=1
		return bites[1:size]
	
	def loop_wr(self, buf, bEndpointAdress, sizeword, size, n, timen, times):
		###Receive data from IMEON in a certain time.

        ###If the read fails for any reason, an :obj:`IOError` exception
        ###is raised.
        
        ###:param buf: the data to send.

        ###:type buf: ASCII
		
		###:param bEndpointAdress: Read adress of the USB port
		
		###:type bEndpointAdress: Hex
		
		###:param sizeword: the max number of bytes that the port can read.

        ###:type sizeword: int

        ###:param size: the total number of bytes to read.

        ###:type size: int
        
        ###:param n: the number of times for the loop.

        ###:type n: int
        
        ###:param timen: recieve data in time seconds.

        ###:type timen: int (in seconds)
        
        ###:param times: recieve data every times seconds.

        ###:type times: int (in seconds)

        ###:return: the data received.

        ###:rtype: list in string'''
		test = 0
		datap=[]
		timeout = time.time() + timen   # time seconds from now	    
		while True:
			#write data
			self.write_datap(buf)
			#read data
			dat=self.loop_read(bEndpointAdress,sizeword,size,n)
			datap.append("".join([chr(x) for x in dat]))
			time.sleep(times)
			if test == 5 or time.time() > timeout:
				break
			test = test - 1
		return datap
