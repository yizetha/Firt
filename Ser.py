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

#----------------------------------------------------------
# code to executate at the set up system.
# Write and read a serial port
#----------------------------------------------------------
start=time.time()
#time.sleep(30)
#----------------------------------------------------------
# 				Connect the serial device
#----------------------------------------------------------
def executeCommand(the_command):
    temp_list = os.popen(the_command).read()
    return temp_list

def getDMESG():
    return executeCommand("dmesg | grep ttyUSB1")
   
def modPROBE():
    return executeCommand("modprobe usbserial vendor=0x067b product=0x2303")
	
#----------------------------------------------------------
#				Turn on the BBB leds on board
#----------------------------------------------------------
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
		
#Connection with the Linux-terminal

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

#----------------------------------------------------------
# 						Main code
#----------------------------------------------------------
if  __name__=="__main__":
	
#---------------Play with the BBB LEDS on board------------
	for x in range(2, 0, -1):
		toggle(x)
	
	#Detect and connect the serial port in Linux
	modPROBE()
	getDMESG()
	
#---------------Wite/Read the Serial port------------------
	
	#find the differents serials ports connects on BBB
	ports=glob.glob('/dev/tty[A-Za-z]*')
	print ports
	for port in ports:
		#If Imeon is not connected, go exit
		if port=='/dev/ttyUSB0':
			#open serial port
			ser = serial.Serial(
				    port='/dev/ttyUSB0',
				    baudrate=2400,
				    parity=serial.PARITY_NONE,
				    stopbits=serial.STOPBITS_ONE,
				    bytesize=serial.EIGHTBITS
				)
			#Create a .dat file
			f=open("/home/debian/Desktop/Code/donnser.dat",'w')
			f.write("Serial port: "+ser.portstr+"\n")
			#Save the date/hour on the .dat
			today=time.localtime()
			type(today)
			f.write(str(today.tm_year) + "/" + str(today.tm_mon) + "/" + str(today.tm_mday) + " " + str(today.tm_hour) + ":" + str(today.tm_min) + ":" + str(today.tm_sec)+"\n")
			#flush input buffer, discarding all its contents
			#ser.flushInput() 
			#flush output buffer, aborting current output 
			#and discard all that is in buffer
			#ser.flushOutput()
			#Read serial port for X minutes
			timeout = time.time() + 5   # 10 minutes from now
			second = 0
			liste=[] #create a list for saving the read data in a .dat file
			while True:
				test = 0  
				if second == 0:
					#Data to write
					data="QPIGS\r"
					#give somme time to seral port
					time.sleep(2)
					#write data to serial port
					ser.write(data) 
					#read data from serial port. The size of reciev data is 136
					reponse = ser.read(136)
					liste.append (reponse)#save in a list		
					second = 1
				#read every 5 seconds
				time.sleep(4)
				#if the time of reading the serial port is done, exit of loop
				if test == 5 or time.time() > timeout:
					break
				else: 							
					#write data
					ser.write(data)  
					#give the serial port somme time to receive the data
					time.sleep(3)
					#read data
					reponse = ser.read(136)
					liste.append (reponse)#save in a list
			    #Exit of while
				test = test - 1	
			#Saving the read data in .dat file
			f.write("Data: "+data+"\n")
			#Convert the read data for being saved
			f.write("\n".join(map(lambda x: x, liste)) + "\n")
			#Turn on the sound in the IMEON
			ser.write("SON\r")
			#give somme minutes to IMEON to respond 
			time.sleep(5)
			#Turn off the sound in the IMEON
			ser.write("SOFF\r")
			#Close the .dat file and the serial port
			f.close()		
			#flush input buffer, discarding all its contents
			ser.flushInput() 
			#flush output buffer, aborting current output 
			#and discard all that is in buffer
			ser.flushOutput()
			ser.close()	
			print "finir"			
#---------------Play with the BBB LEDS on board------------
	atexit.register(set_normal_term)
	set_curses_term()
	for x in range(0, 4, 1):
		toggle(x)
	print ("---%s seconds ---" % (time.time()-start))
	#if len(reponse) != 0:
		#print "read data: " + reponse
	#else:
		#print "ERROR"
