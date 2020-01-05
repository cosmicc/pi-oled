from luma.core.render import canvas
from PIL import ImageFont
from luma.core import cmdline, error
from loguru import logger as log
import os
from time import sleep
from datetime import datetime


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


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(os.path.dirname('/opt/pi-oled/'), 'fonts', name))
    return ImageFont.truetype(font_path, size)


def main():
    device = get_display()
    while True:
        noto14 = make_font("notomono.ttf", 14)
        noto16 = make_font("notomono.ttf", 16)
        noto20 = make_font("notomono.ttf", 20)
        fas = make_font("fa-solid-900.ttf", 25)
        fab = make_font("fa-brands-400.ttf", 25)
        far = make_font("fa-regular-400.ttf", 25)
        with canvas(device) as draw:
            draw.text((0, 0), text="\uf3c5", font=fas, fill="green")
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
