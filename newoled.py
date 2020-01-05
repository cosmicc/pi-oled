import os
from datetime import datetime
from time import sleep

from loguru import logger as log
from luma.core import cmdline, error
from luma.core.render import canvas
from PIL import ImageFont

def make_font(name, size):
    font_path = os.path.abspath(os.path.join(os.path.dirname('/opt/pi-oled/'), 'fonts', name))
    return ImageFont.truetype(font_path, size)


noto14 = make_font("notomono.ttf", 14)
noto16 = make_font("notomono.ttf", 16)
noto20 = make_font("notomono.ttf", 20)
fas = make_font("fa-solid-900.ttf", 25)
fab = make_font("fa-brands-400.ttf", 25)
far = make_font("fa-regular-400.ttf", 25)


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
    except error.Error as e:
        parser.error(e)
        exit(1)
    else:
        return device


def main():
    device = get_display()
    while True:
        with canvas(device) as draw:
            with open("/dev/shm/gps") as gpsfile:
                gpsdata = gpsfile.readline()
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
                    elif gpssplit[0] == 'maiden':
                        gpsmaiden = gpssplit[1]
                        draw.text((0, 50), text=f"  {gpsmaiden}", font=noto16, fill="yellow")
                    else:
                        pass
                    gpsdata = gpsfile.readline()


            draw.text((30, 0), text="\uf017", font=far, fill="green")
            draw.text((68, 0), text="\uf863", font=fas, fill="green")
            draw.text((105, 0), text="\uf2ca", font=fas, fill="green")
            draw.text((0, 27), text=f" {datetime.now().strftime('%H:%M:%S')}", font=noto20, fill="white")
        sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting')
        exit(0)
