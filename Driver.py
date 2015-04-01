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

"""Communications protocols, using PyUSB v1.0.
This module handles the communication with the IMEON
via the USB, RS232 (serial) 
"""
from __future__ import division
import math
from device_usb import *
from device_serial import *
from textdat import *
import glob
import os
from R232COMProtocol import *


def Detport(idport):
	'''Detect the devices connects to the BBB.

	:param port: the device port name, for example '/dev/ttyUSB0'.

	:type port: string'''
			
	#Find all the devices connects to port
	ports=glob.glob(idport)
	if ports:
		if 'Serial Port' in os.popen("lsusb").read():
			#get the name of the port
			port="".join(map(lambda x: x, ports))
			return (True,port)
		if 'USB' in os.popen("lsusb").read():
			return (True, idport)
	else: 
		return (False,idport)
		
def portUSB(port,mbed_vendor_id,mbed_product_id,buf,timen,times):
	'''Detect the USB port on the BBB and play with it
	
	:param port: the device port name, for example '/dev/ttyUSB0'.

	:type port: string
	
	:param mbed_vendor_id: the USB vendor ID number for example 0x1941

    :type mbed_vendor_id: int

    :param mbed_product_id: the USB product ID number for example 0x8021

    :type mbed_product_id: int
    
	:param buf: the data to send 
	
	:type buf: string (ASCII)
		
	:param timen: recieve data in time seconds      
	
	:type timen: int in seconds
	
	:param times: recieve data every times seconds 
	
	:type times: int in seconds
	
	:param return: the data received 
	
	:type return: list in string'''
	#Get the size of the instruction that we are goint to receive form IMEON
	size=int(lisProt(buf))
	###:param size: the total number of bytes to read 
	###:type size: int
	isconnect, portp= Detport(port)
	if isconnect==False:
		print "IMEON not USB connection."
	else:
		print "IMEON USB detect."
		#Recognize the USB port of IMEON
		dev=USBDevice(idVendor=mbed_vendor_id,idProduct=mbed_product_id)
		endpoint=dev.endpoint_dev()
		n=int(math.ceil(size/endpoint.wMaxPacketSize))
		#Recieve datas from USB port
		###loop_wr(buf, bEndpointAdress, sizeword, size, n, timen, times)
        ###buf: the data to send (ASCII)
        ###bEndpointAdress: Read adress of the USB port(int)
        ###sizeword: the max number of bytes that the port can read (int)
		###size: the total number of bytes to read (int)
        ###n: the number of times for the loop.  
        ###timen: recieve data in time seconds(int in seconds)      
        ###times: recieve data every times seconds (int in seconds
        ###return: the data received (list in string)
		pardata=dev.loop_wr(buf,endpoint.bEndpointAddress,endpoint.wMaxPacketSize,size,n,timen,times)
		print "Recieving datas from USB."
		return pardata
	
def portSER(port,buf,timen,times):
	'''Detect the serial port on the BBB and play with it
	
	:param buf: the data to send 
	
	:type buf: string (ASCII)
	
	:param size: the number of bytes to read 
	
	:type size: int
	
	:param timen: recieve data in time seconds      
	
	:type timen: int in seconds
	
	:param times: recieve data every times seconds 
	
	:type times: int in seconds
	
	:param return: the data received 
	
	:type return: list in string'''
	
	#Get the size of the instruction that we are goint to receive form IMEON
	size=int(lisProt(buf))
	###:param size: the total number of bytes to read 
	###:type size: int
	isconnect, ports= Detport(port)
	if isconnect==False:
		print "IMEON not serial connection."
	else:
		print "IMEON RS232 detect."
		#Open serial port
		ser=TTYDevice(ports)
		
		#Recieve datas from serial port
		###loops_wr(self, buf, size, timen, times)
        ###buf: the data to send (ASCII)
        ###size: the number of bytes to read (int)       
        ###timen: recieve data in time seconds(int in seconds)      
        ###times: recieve data every times seconds (int in seconds
        ###return: the data received (list in string)
		print "Recieving datas from RS232."
		serdata=ser.loops_wr(buf,size,timen,times)
		return serdata
	
	#def saveDat(self,nom,buf,datas):	
		##Save datas recieved in .dat file
		#print "sauvegarder des donnees"
		#nom="/home/debian/Desktop/Code/donns.dat"
		#Text(nom,par='n')
		#Text(nom,par='e',data=buf,liste=datas)
