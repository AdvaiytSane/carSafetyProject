import time
import cv2
# import libcamera
from picamera2 import Picamera2
import RPi.GPIO as gpio
import dht11
import lcd_1602
from RiskAssessment import RiskAssessment
import sounddevice as sd
import audioAssesment
import requests

lcd_1602.init(0x27, 1)
   
gpio.setmode(gpio.BCM)
myDHT = dht11.DHT11(pin = 17)
t = 0
cnt = 20
try:
    while cnt > 10:
        # print("reading at :", time.time())
        result = myDHT.read()
        if result.is_valid():
            t = result.temperature
            h = result.humidity
            print("Temperature is " , t, h," at ", time.time())
        time.sleep(0.2)
        cnt  = cnt -1

except KeyboardInterrupt:
    gpio.cleanup()
    print("gpio good to go lesgo")

piCam = Picamera2()
piCam.preview_configuration.main.size = (1280, 720)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()  
riskAss = RiskAssessment()
try:
    while True:
        # print("attempted reading at :", time.time())
        result = myDHT.read()
        if result.is_valid():
            t = result.temperature
            h = result.humidity
            print("Temperature is " , t, h," at ", time.time())
            lcd_1602.write(0,0, "Temp is {0}".format(t))
            
        frame =  piCam.capture_array()
        print("started recording!!")
        audioSample = audioAssesment.recordSample()
        print("finished recording!!")
        riskAss.update(t, frame, audioSample)
        message = riskAss.notify()
        if False:
            resp = requests.post('https://textbelt.com/text', {
                        'phone': '6692514210',
                        'message': message,
                        'key': 'af71119ada56b527242e3f862f3e4e400817350bO0eyayo2OU1Ljs7Ums3bWbmvd',
                        })
        lcd_1602.write(0,1, message)
        isFaceDetected = riskAss.is_face()    
        if isFaceDetected:     
            # Overlay facedetection on image
            face_locations = riskAss.get_face()
            # print("baby detected and temperature above 80 degrees! Please check your car. ")
            for x, y, w, h  in face_locations:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # if riskAss.temp_warning():
        #     print("Warn! High Temp!")
        #     if isFaceDetected:
        #         lcd_1602.write(0,1, "Danger! Baby in High Temp!")
        # else:
        #     if isFaceDetected:
        #         lcd_1602.write(0,1, "Warn! Baby onboard!")
        #     else:
        #         lcd_1602.write(0,1, "  Safe!       ")
        
        cv2.imshow("piCam", frame)

        if cv2.waitKey(1) == ord('q'):
            break

        time.sleep(0.2)

except KeyboardInterrupt:
    gpio.cleanup()
    print("gpio good to go lesgo")
    lcd_1602.clear()
    print("Hrun dzat shiet baeck")