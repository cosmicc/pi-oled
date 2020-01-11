#!/usr/bin/env python3

import os
from datetime import datetime
from pathlib import Path
from time import sleep

import netifaces as ni
from loguru import logger as log
from luma.core import cmdline, error
from luma.core.render import canvas
from PIL import ImageFont


def main():
    def make_font(name, size):
        font_path = os.path.abspath(os.path.join(os.path.dirname('/opt/pi-oled/'), 'fonts', name))
        return ImageFont.truetype(font_path, size)

    noto12 = make_font("notomono.ttf", 12)
    noto14 = make_font("notomono.ttf", 14)
    noto16 = make_font("notomono.ttf", 16)
    noto20 = make_font("notomono.ttf", 20)
    fas = make_font("fa-solid-900.ttf", 25)
    fas2 = make_font("fa-solid-900.ttf",18)
    fab = make_font("fa-brands-400.ttf", 25)
    far = make_font("fa-regular-400.ttf", 25)
    gps_file = Path('/dev/shm/gps')
    net_file = Path('/dev/shm/network')
    hs_file = Path('/dev/shm/hotspot')
    tmp_file = Path('/dev/shm/cputemp')
    throttle_file = Path('/dev/shm/throttle')

    while not gps_file.exists() or not net_file.exists() or not hs_file.exists() or not tmp_file.exists():
        sleep(1)
    log.debug('File checks passed. continuing...')

    def get_display():
        parser = cmdline.create_parser(description='luma.examples arguments')
        try:
            config = cmdline.load_config('/etc/oled.conf')
            args = parser.parse_args(config)
        except:
            log.exception('No display configuration found (/etc/oled.conf)')
            exit(1)
        try:
            device = cmdline.create_device(args)
            log.info('Display Initilized')
        except error.Error as e:
            parser.error(e)
            exit(1)
        else:
            return device

    device = get_display()
    log.debug('Starting main loop')
    while True:
        with canvas(device) as draw:
            # GPS DATA
            with open(str(gps_file)) as gpsfile:
                gpsdata = gpsfile.readline()
                log.debug('Reading GPS data file')
                while gpsdata:
                    gpssplit = gpsdata.strip('\n').split('=')
                    if gpssplit[0] == 'fix':
                        gpsfix = gpssplit[1]
                        if gpsfix == 'No GPS':
                            fcolor = "red"
                        elif gpsfix == 'No Fix':
                            fcolor = "yellow"
                        elif gpsfix == '2D Fix' or gpsfix == '3D Fix':
                            fcolor = "green"
                        else:
                            fcolor = "grey"
                        draw.text((0, 0), text="\uf3c5", font=fas, fill=fcolor)
                    elif gpssplit[0] == 'timesource':
                        timesource = gpssplit[1]
                        if timesource == 'PPS':
                            fcolor = "green"
                        elif timesource == "NIST" or timesource == "GPS":
                            fcolor = "yellow"
                        else:
                            fcolor = "dimgray"
                        draw.text((32, 0), text="\uf017", font=far, fill=fcolor)
                    elif gpssplit[0] == 'maiden':
                        gpsmaiden = gpssplit[1]
                        if gpsmaiden == "JJ00aa00":
                            gpsmaiden = "No Maidenhead"
                        else:
                            gpsmaiden = "  " + gpsmaiden
                        draw.text((0, 65), text=f"{gpsmaiden}", font=noto16, fill="yellow")
                    else:
                        pass
                    gpsdata = gpsfile.readline()
            # HOTSPOT DATA
            log.debug('Reading HOTSPOT data file')
            with open(str(hs_file)) as hsfile:
                hsdata = hsfile.readline()
            log.debug('Reading NET data file')
            with open(str(net_file)) as netfile:
                netdata = netfile.readline()
                while netdata:
                    netsplit = netdata.strip('\n').split('=')
                    if netsplit[0] == 'internet':
                        internet = netsplit[1]
                    elif netsplit[0] == 'bitrate':
                        bitrate = netsplit[1]
                    elif netsplit[0] == 'band':
                        band = netsplit[1]
                    elif netsplit[0] == 'quality':
                        quality = netsplit[1]
                    elif netsplit[0] == 'signal_percent':
                        signal = netsplit[1]
                        if len(signal) == 2:
                           signal = f'  {signal}'
                        elif len(signal) == 1:
                           signal = f'   {signal}'
                        elif len(signal) == 3:
                           signal = f' {signal}'
                    else:
                        pass
                    netdata = netfile.readline()
            if hsdata == "True":
                fcolor = "blue"
                draw.text((0, 85), text="Hotspot Clients: 0", font=noto14, fill="cyan")
            elif internet == "True":
                fcolor = "green"
                draw.text((0, 85), text=f"{band}{signal}%  {bitrate}", font=noto14, fill="cyan")
            else:
                fcolor = "yellow"
            draw.text((68, 0), text="\uf1eb", font=fas, fill=fcolor)
            # IP DATA
            log.debug('Reading IP data')
            try:
                wip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
            except:
                wip = "No Address"
            try:
                eip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
            except:
                eip = "No Address"
            draw.text((0, 116), text=f"wlan: {wip}", font=noto12, fill="orange")
            draw.text((0, 101), text=f"eth: {eip}", font=noto12, fill="orange")
            # TEMP DATA
            log.debug('Reading Temperature data file')
            with open(str(tmp_file)) as tempfile:
                tempdata = int(tempfile.readline())
            if tempdata < 60:
                fcolor = "green"
            elif tempdata > 70:
                fcolor = "red"
            else:
                fcolor = "yellow"
            draw.text((110, 0), text="\uf2ca", font=fas, fill=fcolor)
            draw.text((0, 27), text=f" {datetime.now().strftime('%H:%M:%S')}", font=noto20, fill="white")
            # UNDERVOLT & OVERTEMP ALARM
            log.debug('Reading undervolt and overtemp data file')
            with open(str(throttle_file)) as throttlefile:
                throttledata = throttlefile.readline()
                while throttledata:
                    tsplit = throttledata.strip('\n').split('=')
                    if tsplit[0] == 'undervolt_hist':
                        undervolt = tsplit[1]
                    elif tsplit[0] == 'throttle_hist':
                        throttle = tsplit[1]
                    throttledata = throttlefile.readline()
            if undervolt == 'True':
                draw.text((0, 30), text="\uf0e7", font=fas2, fill="red")
            if throttle == "True":
                draw.text((111, 28), text="\uf2db", font=fas2, fill="red")
        log.debug('Sleep wait')
        sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting')
        exit(0)
