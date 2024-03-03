import time
import cv2
# import libcamera
from picamera2 import Picamera2
import RPi.GPIO as gpio
import dht11
import lcd_1602
from RiskAssessment import RiskAssessment

lcd_1602.init(0x27, 1)

    
gpio.setmode(gpio.BCM)
myDHT = dht11.DHT11(pin = 17)
t = 0

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
            isValdTemp = True
            print("Temperature is " , t, h," at ", time.time())
            lcd_1602.write(0,0, "Temp is {0}".format(t))
            
        frame =  piCam.capture_array()
        riskAss.update(t, frame)
        isFaceDetected = riskAss.is_face()    
        if isFaceDetected:
            # Overlay facedetection on image
            face_locations = riskAss.get_face()
            # print("baby detected and temperature above 80 degrees! Please check your car. ")
            for x, y, w, h  in face_locations:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if riskAss.temp_warning():
            lcd_1602.write(0,1, "Warn! High Temp!")
            if isFaceDetected:
                lcd_1602.write(0,1, "Danger! Baby in High Temp!")
        else:
            if isFaceDetected:
                lcd_1602.write(0,1, "Warn! Baby onboard!")
            else:
                lcd_1602.write(0,1, "  Safe!       ")
        cv2.imshow("piCam", frame)

        if cv2.waitKey(1) == ord('q'):
            break

        time.sleep(0.2)

except KeyboardInterrupt:
    gpio.cleanup()
    print("gpio good to go lesgo")
    lcd_1602.clear()
    print("Hrun dzat shiet baeck")