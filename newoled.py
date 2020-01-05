from luma.core.render import canvas
from PIL import ImageFont
from luma.core import cmdline, error

df get_display():
    try:
        config = cmdline.load_config('/etc/oled.conf')
        args = parser.parse_args(config)
    except:
        print('No display configuration found (/etc/oled.conf)')
        exit(1)
    try:
        device = cmdline.create_device(args)
    except error.Error as e:
        parser.error(e)
        exit(1)
    else:
        return device


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)


def main():
    device = get_device()
    font = make_font("motomono.ttf", 14)
    with canvas(device) as draw:
        draw.text((50, 50), text="hello world", font=font, fill="white")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting')
        exit(0)