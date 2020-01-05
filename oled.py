# -*- coding:UTF-8 -*-

#--------------Driver Library-----------------#
import RPi.GPIO as GPIO
import OLED_Driver as OLED
#--------------Image Library---------------#
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
#-------------Test Display Functions---------------#


def Test_Text():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('cambriab.ttf', 24)

    draw.text((0, 12), 'WaveShare', fill="BLUE", font=font)
    draw.text((0, 36), 'Electronic', fill="BLUE", font=font)
    draw.text((20, 72), '1.5 inch', fill="CYAN", font=font)
    draw.text((10, 96), 'R', fill="RED", font=font)
    draw.text((25, 96), 'G', fill="GREEN", font=font)
    draw.text((40, 96), 'B', fill="BLUE", font=font)
    draw.text((55, 96), ' OLED', fill="CYAN", font=font)

    OLED.Display_Image(image)


#----------------------MAIN-------------------------#
try:

    def main():

        #-------------OLED Init------------#
        OLED.Device_Init()
        Test_Text()

    if __name__ == '__main__':
        main()

except:
    print("\r\nEnd")
    OLED.Clear_Screen()
    GPIO.cleanup()


