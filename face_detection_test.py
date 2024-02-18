import time
import RPi.GPIO as gpio
import dht11
import cv2
# import matplotlib.pyplot as plt
from RiskAssessment import RiskAssessment
from picamera2 import Picamera2
# define a video capture object
# cap = cv2.VideoCapture(0)

gpio.setmode(gpio.BCM)

piCam = Picamera2()
piCam.preview_configuration.main.size = (1280, 720)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

try:
    while True:
        fr_ = piCam.capture_array()
        cv2.imshow("piCam", fr_)
        if cv2.waitkey(1) == ord('q'):
           break
        time.sleep(0.2)

except KeyboardInterrupt:
    gpio.cleanup()
    print("gpio good to go lesgo")
    
exit()

if not piCam.isOpened():
    print("Cannot open camera")
    piCam.release()
    cv2.destroyAllWindows()
    exit()
else:
    print(piCam)
temperature = 90

# only do this while temperature is above 80
while (temperature > 80):
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        print(frame)
        cap.release()
        cv2.destroyAllWindows()
        break

    ass = RiskAssessment(temperature, frame)
    if ass.notify():
        print("baby detected and temperature above 80 degrees! Please check your car. ")
    else:
        print("baby not detected.")
