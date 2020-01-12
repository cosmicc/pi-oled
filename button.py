import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.wait_for_edge(21, GPIO.RISING)

def button_press(input_pin):
    print('button press!')
    time.sleep(5)

GPIO.add_event_detect(21, GPIO.RISING, callback=button_press)

while True:
    time.sleep(120)
