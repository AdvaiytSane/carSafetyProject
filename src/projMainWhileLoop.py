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

# Setup inputs
lcd_1602.init(0x27, 1)   
gpio.setmode(gpio.BCM)
myDHT = dht11.DHT11(pin = 17)
piCam = Picamera2()
piCam.preview_configuration.main.size = (1280, 720)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()  

riskAss = RiskAssessment()

idTask = 0 #0: Temp, #1: Camera, #2, Audio
timePeriods = [4.0, 6.0, 6.0] # ms Time Periods for each tasks

try:
    while True:
        if idTask == 0: # Temperature update
            startTime = time.time()
            print(f"Running Temp Task at {startTime}")
            while time.time() < startTime + timePeriods[idTask]:
                # print("attempted reading at :", time.time())
                result = myDHT.read()
                if result.is_valid():
                    t = result.temperature
                    h = result.humidity
                    print("Temperature is " , t, h," at ", time.time())
                    riskAss.updateTemp(t)
                    lcd_1602.write(0,0, "Temp is {0}".format(t))
        elif idTask == 1: # cameraTask
            startTime = time.time()
            print(f"Running Camera Task at {startTime}")
            while (time.time() < startTime + timePeriods[idTask]):
                frame =  piCam.capture_array()
                riskAss.updateImageFrame(frame)
                isFaceDetected = riskAss.is_face()    
                if isFaceDetected: # Overlay facedetection on image
                    face_locations = riskAss.get_face()
                    for x, y, w, h  in face_locations:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.imshow("piCam", frame)                
                if cv2.waitKey(1) == ord('q'):
                    break
        elif (idTask == 2): # Audio Task           
            startTime = time.time()    
            print(f"Running Audio Task at {startTime}")         
            print("started recording at {startTime}!!")
            audioSample = audioAssesment.recordSample()
            riskAss.updateAudioSample(audioSample)
            duration = time.time() - startTime
            print("finished recording and classification in {duration} sec.")
        else:
            print("ERROR: incorrect idTask")

        idTask = (idTask + 1) % 3
        if idTask == 0: # All tasks are completed.
            # riskAss.update(t, frame, audioSample)
            message = riskAss.notify()
            print(message)
            # Change this: if its a bad situation text the parent
            # resp = requests.post('https://textbelt.com/text', {
            #             'phone': '6692514210',
            #             'message': message,
            #             'key': 'af71119ada56b527242e3f862f3e4e400817350bO0eyayo2OU1Ljs7Ums3bWbmvd',
            #             })
            lcd_1602.write(0,1, message)

except KeyboardInterrupt:
    gpio.cleanup()
    print("gpio good to go lesgo")
    lcd_1602.clear()
    print("Hrun dzat shiet baeck")