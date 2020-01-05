#!/usr/bin/env python3

import OLED_Driver as OLED
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
from time import sleep
import netifaces as ni
from datetime import datetime

gpsgreen = Image.open("/opt/pi-oled/images/gps-green.jpg")
gpsyellow = Image.open("/opt/pi-oled/images/gps-yellow.jpg")
gpsred = Image.open("/opt/pi-oled/images/gps-red.jpg")
tempgreen = Image.open("/opt/pi-oled/images/temp-green.jpg")
fangreen = Image.open("/opt/pi-oled/images/fan-green.jpg")
hotspotgreen = Image.open("/opt/pi-oled/images/hotspot-green.jpg")
hotspotgrey = Image.open("/opt/pi-oled/images/hotspot-grey.jpg")
timegreen = Image.open("/opt/pi-oled/images/time-grey.jpg")

font20 = ImageFont.truetype('/opt/pi-oled/fonts/notomono.ttf', 20)
font16 = ImageFont.truetype('/opt/pi-oled/fonts/notomono.ttf', 16)
font14 = ImageFont.truetype('/opt/pi-oled/fonts/notomono.ttf', 14)
font11 = ImageFont.truetype('/opt/pi-oled/fonts/notomono.ttf', 11)
font12 = ImageFont.truetype('/opt/pi-oled/fonts/notomono.ttf', 12)
font8 = ImageFont.truetype('/opt/pi-oled/fonts/notomono.ttf', 9)


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
                elif gpsfix == 'No Fix':
                    image.paste(gpsyellow, (5, 0))
                elif gpsfix == '2D Fix' or gpsfix == '3D Fix':
                    image.paste(timegreen, (5, 0))
                else:
                    image.paste(gpsred, (5, 0))
            elif gpssplit[0] == 'maiden':
                gpsmaiden = gpssplit[1]
                draw.text((5, 50), gpsmaiden, fill="GREEN", font=font14)
            else:
                pass
            gpsdata = gpsfile.readline()


def gettime():
    draw.text((0, 26), f' {datetime.now().strftime("%H:%M:%S")}', fill="WHITE", font=font20)


def hotspot():
    draw.text((0, 85), f'Hotspot Clients: 4', fill="CYAN", font=font12)
    OLED.Display_Image(image)


OLED.Device_Init()
image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
try:
    while True:
        draw = ImageDraw.Draw(image)
        gps_status()
        image.paste(tempgreen, (115, 0))
        image.paste(fangreen, (80, 2))
        image.paste(hotspotgrey, (45, 2))
        getips()
        hotspot()
        gettime()
        # OLED.Clear_Screen()
        OLED.Display_Image(image)

        sleep(1)
except:
    print("\r\nEnd")
    OLED.Clear_Screen()
    GPIO.cleanup()

OLED.Clear_Screen()
GPIO.cleanup()
