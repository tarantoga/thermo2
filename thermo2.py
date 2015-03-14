# -*- coding: ascii -*-
import serial
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import Image
import ImageDraw
import ImageFont
import redis
 
# Raspberry Pi pin configuration:
RST = 24
 
# Serial configuration:
DEVICE = '/dev/ttyAMA0'
BAUD = 9600
 
# 128x32 display with hardware I2C:#
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()
 
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
 
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = 1
shape_width = 20
top = padding
bottom = height-padding
x = padding
font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 32)
font1 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 24)
font2 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
font3 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 10)

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

        #remember last 2880 commands (with measurement each 30 seconds it gives 24h history for debug reasons)
        r.lpush(address, command)
        r.ltrim(address, 0, 2879)

        if command.startswith("TMPA"):
                temp = command[4:]
                ftemp = float(temp)
                r.lpush("%sval" % address, round(ftemp, 1)) #remember value
                r.ltrim("%sval" % address, 0, 2879)
                print("%s temp: %.1f" % (t, ftemp))
 
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((x, top), "%.1f" % ftemp, font=font, fill=255)
                draw.text((x + 85, top), "o", font=font2, fill=255)
                draw.text((x + 95, top), "C", font=font1, fill=255)
                draw.text((x + 80, top + 20), "%s" % t, font=font3, fill=255)
                
                disp.image(image)
                disp.display()

        elif command.startswith("BATT"):
                batt = command[4:-1]
                fbatt = float(batt)

                r.set("%sbat" % address, fbatt) #remember last battery voltage
                print("%s batt: %.1f" % (t, fbatt))





                
