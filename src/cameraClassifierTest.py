import time
import cv2
# import libcamera
from picamera2 import Picamera2
from RiskAssessment import RiskAssessment

# Setup inputs
piCam = Picamera2()
piCam.preview_configuration.main.size = (1280, 720)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()  

riskAss = RiskAssessment()

while True:
    startTime = time.time()
    print(f"Running Camera Task at {startTime}")
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