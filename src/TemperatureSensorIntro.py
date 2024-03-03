import time
import RPi.GPIO as gpio
import dht11
gpio.setmode(gpio.BCM)
myDHT = dht11.DHT11(pin = 17)
t = 0

try:
    while True:
        print("reading at :", time.time())
        result = myDHT.read()
        if result.is_valid():
            t = result.temperature
            h = result.humidity
            print("Temperature is " , t, h," at ", time.time())
        time.sleep(0.2)

except KeyboardInterrupt:
    gpio.cleanup()
    print("gpio good to go lesgo")