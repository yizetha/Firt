import os
import sys
 
import usb.core
import usb.util
import usb.legacy

import time

start=time.time()
# handler called when a report is received
def rx_handler(data):
	print 'recv: ', data
 
def findHIDDevice(mbed_vendor_id, mbed_product_id):
	#Find USB device
	hid_device = usb.core.find(idVendor=mbed_vendor_id,idProduct=mbed_product_id)
	if not hid_device:
		print "No device connected"
	else:
		#Create a txt file
		f=open("/home/debian/Desktop/Code/donnes.dat",'w')
		f.write("USB"+"\n")
		today=time.localtime()
		type(today)
		f.write(str(today.tm_mday) + "/" +str(today.tm_mon) + "/" +  str(today.tm_year) + " " + str(today.tm_hour) + ":" + str(today.tm_min) + ":" + str(today.tm_sec)+"\n")
		#sys.stdout.write(' \n')
		#sys.stdout.write('Device found\n')
		endpoint = hid_device[0][(0,0)][0]
		try:
			detach = hid_device.is_kernel_driver_active(0)
		except NotImplementedError:
			detach = True
		if detach:
			try:
				hid_device.detach_kernel_driver(0)
			except usb.core.USBError as e:
				sys.exit("Could not detatch kernel driver: %s" % str(e))
		hid_device.reset()
		hid_device.set_configuration()
		usb.util.claim_interface(hid_device,0)
		
		data = "QPIGS\r"
		
		#Get the endpoint out for writing
		bmRequestType=usb.util.build_request_type(
			usb.util.ENDPOINT_OUT,
			usb.util.CTRL_TYPE_CLASS,
			usb.util.CTRL_RECIPIENT_INTERFACE
			)
		#Read USB for 1 minute
		timeout = time.time() + 5   # 1 minute from now
		second = 0
		a=[]
		while True:
			test = 0	    
			if second == 0:
				#write data
				hid_device.ctrl_transfer(
					bmRequestType=bmRequestType, 
					bRequest=usb.REQ_SET_CONFIGURATION,
					data_or_wLength=data,
					wValue=0,
					timeout=0)	
				#read data
				bites=[]
				i=0
				while i<17:
					bites+=hid_device.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize,0)
					i+=1
				a.append("".join([chr(x) for x in bites]))
				second = 1
			time.sleep(5)
			if test == 5 or time.time() > timeout:
				break
			else: 	
				#write data
				hid_device.ctrl_transfer(
					bmRequestType=bmRequestType, 
					bRequest=usb.REQ_SET_CONFIGURATION,
					data_or_wLength=data,
					wValue=0,
					timeout=0)	
				#read data
				bites=[]
				i=0
				while i<17:
					bites+=hid_device.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize,0)
					i+=1
				a.append("".join([chr(x) for x in bites]))
				second = 1
			test = test - 1
		f.write("Data from: "+data+"\n")
		f.write("\n".join(map(lambda x: x, a)) + "\n")
		f.close()
		#hid_device.attach_kernel_driver(0)
		
if __name__ == '__main__':
# The vendor ID and product ID used in the Mbed program
	mbed_vendor_id = 1637 
	mbed_product_id = 20833
	
# Search the Mbed, attach rx handler and send data
	findHIDDevice(mbed_vendor_id, mbed_product_id)
	
print ("---%s seconds ---" % (time.time()-start))
