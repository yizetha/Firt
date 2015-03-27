#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2015 Demo User <debian@beaglebone>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import struct
import serial
import time
import sys
import os
import random
import termios
import atexit
import glob
from select import select

#time.sleep(30)
#------------------------------------------
#Connect to serial port
def executeCommand(the_command):
    temp_list = os.popen(the_command).read()
    return temp_list

def getDMESG():
    return executeCommand("dmesg | grep ttyUSB0")
   
def modPROBE():
    return executeCommand("modprobe usbserial vendor=0x067b product=0x2303")
	
#-------------------------------------------
#Turn on the on board leds
#-------------------------------------------
leds = ['/sys/class/leds/beaglebone:green:usr0/brightness',
		'/sys/class/leds/beaglebone:green:usr1/brightness',
		'/sys/class/leds/beaglebone:green:usr2/brightness',
		'/sys/class/leds/beaglebone:green:usr3/brightness',
		]

def ledon(n):
        value = open(leds[n],'w')
        value.write(str(1))
        value.close()

def ledoff(n):
        value = open(leds[n],'w')
        value.write(str(0))
        value.close()
 
def toggle(x):
		ledoff(x)
		time.sleep(0.1)
		ledon(x)
		
for i, val in enumerate(leds):
		ledoff(i)
 
# save the terminal settings
fd = sys.stdin.fileno()
new_term = termios.tcgetattr(fd)
old_term = termios.tcgetattr(fd)
 
# new terminal setting unbuffered
new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)
 
# switch to normal terminal
def set_normal_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)
 
# switch to unbuffered terminal
def set_curses_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)

if  __name__=="__main__":

	#Detect the serial port
	modPROBE()
	getDMESG()
	
	#--------------------------------------
	#Serial port
	#--------------------------------------
	ports=glob.glob('/dev/tty[A-Za-z]*')
	#If Imeon is not connected, go exit
	for port in ports:
		if port=='/dev/ttyUSB0':
			#open serial port			
			ser = serial.Serial(
				    port='/dev/ttyUSB0',
				    baudrate=2400,
				    parity=serial.PARITY_NONE,
				    stopbits=serial.STOPBITS_ONE,
				    bytesize=serial.EIGHTBITS
				)
			#Create a txt file
			f=open("/home/debian/Desktop/Code/donnes.txt",'w')
			f.write("Serial port: "+ser.portstr+"\n")
			today=time.localtime()
			type(today)
			f.write(str(today.tm_year) + "/" + str(today.tm_mon) + "/" + str(today.tm_mday) + " " + str(today.tm_hour) + ":" + str(today.tm_min) + ":" + str(today.tm_sec)+"\n")
			ser.flushInput() #flush input buffer, discarding all its contents
			ser.flushOutput()#flush output buffer, aborting current output 
			                 #and discard all that is in buffer
			
			#Read serial port for 1 minute
			timeout = time.time() + 10   # 1 minute from now
			second = 0
			a=[]
			while True:
				test = 0  
				if second == 0:
					#write data
					data="QPIGS\r"
					#read data
					time.sleep(1)
					ser.write(data) 
					reponse = ser.read(136)
					a.append (str(reponse))
					#f.write("Data: "+data+"\n")
					#f.write(reponse+"\n")			
					#time.sleep(1)  #give the serial port some time to receive the data
					second = 1
				time.sleep(4)
				if test == 5 or time.time() > timeout:
					break
				else: 							
					#write data
					ser.write(data)  
					#read data
					time.sleep(1)
					reponse = ser.read(136)
					a.append (str(reponse))
					#f.write(reponse+"\n")
					#time.sleep(1)  #give the serial port some time to receive the data
			    #Exit of while
				test = test - 1	
			f.write("Data: "+data+"\n")
			f.write("\n".join(map(lambda x: str(x), a)) + "\n")
			#ser.write("SON\r")
			#print "sound on"
			#time.sleep(5)
			#ser.write("SOFF\r")
			#print "sound off"
			f.close()		
			ser.close()				
	#---------------Leds------------
	atexit.register(set_normal_term)
	set_curses_term()
	for x in range(0, 4, 1):
		toggle(x)
 
	#for x in range(2, 0, -1):
		#toggle(x)

	#if len(reponse) != 0:
		#print "read data: " + reponse
	#else:
		#print "ERROR"
