#!/usr/bin/env python3

import OLED_Driver as OLED
import RPi.GPIO as GPIO
from PIL import Image, ImageColor, ImageDraw, ImageFont
from time import sleep

gpsgreen = Image.open("gps-green.jpg")
gpsyellow = Image.open("gps-yellow.jpg")
gpsred = Image.open("gps-red.jpg")
tempgreen = Image.open("temp-green.jpg")

font1 = ImageFont.truetype('notomono.ttf', 16)

def gps_status():
    print('running gps_status')
    with open("/dev/shm/gps") as gpsfile:
        gpsdata = gpsfile.readline()
        while gpsdata:
            gpssplit = gpsdata.strip('\n').split('=')
            if gpssplit[0] == 'fix':
                gpsfix = gpssplit[1]
                if gpsfix == 'No GPS':
                    image.paste(gpsred, (5, 0))
                    OLED.Display_Image(image)
                elif gpsfix == 'No Fix':
                    image.paste(gpsyellow, (5, 0))
                    OLED.Display_Image(image)
                elif gpsfix == '2D Fix' or gpsfix == '3D Fix':
                    image.paste(gpsgreen, (5, 0))
                    OLED.Display_Image(image)
                else:
                    image.paste(gpsred, (5, 0))
                    OLED.Display_Image(image)
            elif gpssplit[0] == 'maiden':
                gpsmaiden = gpssplit[1]
                draw.text((5, 30), gpsmaiden, fill="WHITE", font=font1)                
            else:
                 pass
            gpsdata = gpsfile.readline()


def Test_Text():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    gpsgreen = Image.open("gps-green.jpg")
    gpsyellow = Image.open("gps-yellow.jpg")
    gpsred = Image.open("gps-red.jpg")
    image.paste(gpsgreen, (10, 0))
    image.paste(gpsyellow, (40, 0))
    image.paste(gpsred, (70, 0))
    font1 = ImageFont.truetype('notomono.ttf', 20)
    font2 = ImageFont.truetype('notomono.ttf', 14)

    #draw.text((0, 12), 'WaveShare', fill="BLUE", font=font1)
    # OLED.Display_Image(image)
    #draw.text((0, 36), 'Electronic', fill="BLUE", font=font)
    #draw.text((20, 72), '1.5 inch', fill="CYAN", font=font)
    #draw.text((10, 96), 'R', fill="RED", font=font)
    #draw.text((25, 96), 'G', fill="GREEN", font=font)
    #draw.text((40, 96), 'B', fill="BLUE", font=font)
    draw.text((55, 96), 'sample', fill="GREY", font=font2)

    OLED.Display_Image(image)


OLED.Device_Init()
image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
draw = ImageDraw.Draw(image)
# Test_Text()
try:
    gps_status()
    image.paste(tempgreen, (40, 40))
    print('sleeping')
    sleep(60) 
except:
    print("\r\nEnd")
    OLED.Clear_Screen()
    GPIO.cleanup()

OLED.Clear_Screen()
GPIO.cleanup()
