import RPi.GPIO as gpio
import time, math
gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)

def blinky(t, s):
    n = math.floor(t/s)
    print(n)
    f = True
    for i in range(n):
        gpio.output(11, f)
        time.sleep(s)
        f = not(f)

def blinky2():
    s = input()
    f = True
    for i in s:
        if i == " ":
            time.sleep(0.5)
        else:
            gpio.output(11,f)
            f = not(f)
            time.sleep(0.1)
            gpio.output(11, f,)
            f = not(f)
    
blinky2()
gpio.cleanup()

            

