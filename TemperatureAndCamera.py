import time
import cv2
# import libcamera
from picamera2 import Picamera2
import RPi.GPIO as gpio
import dht11
gpio.setmode(gpio.BCM)
myDHT = dht11.DHT11(pin = 17)
t = 0

piCam = Picamera2()
piCam.preview_configuration.main.size = (1280, 720)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

try:
    while True:

        

        #print("reading at :", time.time())

        result = myDHT.read()
        if result.is_valid():
            t = result.temperature
            h = result.humidity
            print("Temperature is " , t, h," at ", time.time())
        if t > 0:
            frame =  piCam.capture_array()
            cv2.imshow("piCam", frame)
            if cv2.waitKey(1) == ord('q'):
                break
        time.sleep(0.2)

except KeyboardInterrupt:
    gpio.cleanup()
    print("gpio good to go lesgo")