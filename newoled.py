from luma.core.render import canvas
from PIL import ImageFont
from luma.core import cmdline, error
from loguru import logger as log
import os
from time import sleep


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
    print(font_path)
    return ImageFont.truetype(font_path, size)


def main():
    device = get_display()
    noto = make_font("notomono.ttf", 14)
    fa = make_font("notomono.ttf", 20)
    with canvas(device) as draw:
        draw.text((50, 0), text="hello world", font=noto, fill="white")
        draw.text((50, 0), text="\uf3c5", font=fa, fill="green")
    sleep(30)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting')
        exit(0)
