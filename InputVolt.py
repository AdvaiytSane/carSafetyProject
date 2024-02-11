import RPi.GPIO as gpio
from time import sleep
import math

gpio.setmode(gpio.BOARD)
gpio.setup(40,gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup(38,gpio.OUT)
pressed2 = False
prevVal = 2

try:
    while True:
        
        readVal = gpio.input(40)
        print(readVal)
        if readVal == 0 and prevVal == 1: 
            pressed2 = not(pressed2)
        print(pressed2)
        prevVal = readVal
        gpio.output(38, pressed2)
except KeyboardInterrupt:
    gpio.cleanup()
    print("LFGGGG")
