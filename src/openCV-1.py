import cv2
from picamera2 import Picamera2, Preview
import libcamera
import time
piCam = Picamera2()
piCam.preview_configuration.main.size = (1280, 720)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

while True:
    
    frame =  piCam.capture_array()
    cv2.imshow("piCam", frame)
    time.sleep(1)
    if cv2.waitKey(1) == ord('q'):
        break
    

cv2.destroyAllWindows()