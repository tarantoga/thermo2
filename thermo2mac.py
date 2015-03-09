# -*- coding: ascii -*-
import serial
import time
import redis
 
# Raspberry Pi pin configuration:
RST = 24
 
# Serial configuration:
DEVICE = '/dev/tty.usbmodem000001'      # Mac
BAUD = 9600
 
r = redis.StrictRedis(host='localhost', port=6379, db=0)

ser = serial.Serial(DEVICE, BAUD)
while 1:	
	data = ser.read(12)
	print("%s" % data)
        t = time.strftime("%H:%M:%S", time.localtime())
 
        if not data.startswith('a'):
                break
 
        address = data[1:3]
        command = data[3:]
	print("address: %s" % address)
	print("command: %s" % command)

        #check if address already exists, if not add to the list of known addresses
        if not r.sismember('sensors', address):
                r.sadd('sensors', address)

        #remember last 2880 commands (with measurement each 30 seconds it gives 24h history)
        r.lpush(address, command)
        r.ltrim(address, 0, 2879)
  
        if command.startswith("TMPA"):
                temp = command[4:]
                ftemp = float(temp)

                r.lpush("%sval" % address, round(ftemp, 1)) #remember value
                r.ltrim(address, 0, 2879)
                print("%s temp: %.1f" % (t, ftemp))

        elif command.startswith("BATT"):
                batt = command[4:-1]
                fbatt = float(batt)

                r.set("%sbat" % address, fbatt) #remember last battery voltage
                print("%s batt: %.1f" % (t, fbatt))



