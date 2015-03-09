# -*- coding: ascii -*-
import serial
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import Image
import ImageDraw
import ImageFont
 
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
ser = serial.Serial(DEVICE, BAUD)
while 1:	
	data = ser.read(12)
	print("%s" % data)
 
        if not data.startswith('a'):
                break
 
        address = data[1:3]
        command = data[3:]
	print("address: %s" % address)
	print("command: %s" % command)
 
        if command.startswith("TMPA"):
                temp = command[4:]
                ftemp = float(temp)
                
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                
                t = time.strftime("%H:%M:%S", time.localtime())
                print("%s temp: %.1f" % (t, ftemp))
 
                draw.text((x, top), "%.1f" % ftemp, font=font, fill=255)
                draw.text((x + 85, top), "o", font=font2, fill=255)
                draw.text((x + 95, top), "C", font=font1, fill=255)
                draw.text((x + 80, top + 20), "%s" % t, font=font3, fill=255)
                
                disp.image(image)
                disp.display()
