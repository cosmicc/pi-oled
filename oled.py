#!/usr/bin/env python3

import OLED_Driver as OLED
import RPi.GPIO as GPIO
from PIL import Image, ImageColor, ImageDraw, ImageFont
from time import sleep
import netifaces as ni
from datetime import datetime

gpsgreen = Image.open("/opt/pi-oled/gps-green.jpg")
gpsyellow = Image.open("/opt/pi-oled/gps-yellow.jpg")
gpsred = Image.open("/opt/pi-oled/gps-red.jpg")
tempgreen = Image.open("/opt/pi-oled/temp-green.jpg")
fangreen = Image.open("/opt/pi-oled/fan-green.jpg")
hotspotgreen = Image.open("/opt/pi-oled/hotspot-green.jpg")
hotspotgrey = Image.open("/opt/pi-oled/hotspot-grey.jpg")
timegreen = Image.open("/opt/pi-oled/time-grey.jpg")

font20 = ImageFont.truetype('/opt/pi-oled/notomono.ttf', 20)
font16 = ImageFont.truetype('/opt/pi-oled/notomono.ttf', 16)
font14 = ImageFont.truetype('/opt/pi-oled/notomono.ttf', 14)
font11 = ImageFont.truetype('/opt/pi-oled/notomono.ttf', 11)
font12 = ImageFont.truetype('/opt/pi-oled/notomono.ttf', 12)
font8 = ImageFont.truetype('/opt/pi-oled/notomono.ttf', 9)

def getips():
    try:
        wip = ni.ifaddresses('wlan1')[ni.AF_INET][0]['addr']
    except:
        wip = "No Address"
    try:
        eip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    except:
        eip = "No Address"
    draw.text((0, 116), f'wlan: {wip}', fill="YELLOW", font=font11)
    draw.text((0, 102), f'eth: {eip}', fill="YELLOW", font=font11)
    OLED.Display_Image(image)


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
                    image.paste(timegreen, (5, 0))
                    OLED.Display_Image(image)
                else:
                    image.paste(gpsred, (5, 0))
                    OLED.Display_Image(image)
            elif gpssplit[0] == 'maiden':
                gpsmaiden = gpssplit[1]
                draw.text((5, 50), gpsmaiden, fill="GREEN", font=font14)
                OLED.Display_Image(image)                
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
    image.paste(tempgreen, (115, 0))
    image.paste(fangreen, (80, 2))
    image.paste(hotspotgrey, (45, 2))
    draw.text((0, 85), f'Hotspot Clients: 4', fill="CYAN", font=font12)
    draw.text((0, 26), f' {datetime.now().strftime("%H:%M:%S")}', fill="WHITE", font=font20)
    OLED.Display_Image(image)
    getips()
    print('sleeping')
    sleep(60) 
except:
    print("\r\nEnd")
    OLED.Clear_Screen()
    GPIO.cleanup()

OLED.Clear_Screen()
GPIO.cleanup()
