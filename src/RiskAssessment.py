import cv2
import audioAssesment
import numpy as np


class RiskAssessment:
    def __init__(self, temp=0, frame=None, audio=None):
        self.temp = temp
        self.frame = frame
        # self.face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # self.face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.face_classifier = cv2.CascadeClassifier('/home/advaiytsane/Downloads/haarcascade_frontalface_default.xml')
        self.face = None
        self.audio = audio
        self.babyNoise = None
        self.hazard = False

    def get_temp(self):
        return self.temp

    def get_raw_frame(self):
        return self.frame
    
    def get_face(self):
        return self.face
    
    def updateImageFrame(self, frame):
        self.frame = frame
        self.face_detection()
    
    def updateAudioSample(self, audio):
        self.audio = audio
        self.audio_detection()

    def updateTemp(self, temp):
        self.temp = temp
    
    def runClassification(self):
        self.face_detection()
        self.audio_detection()


    def update(self, temp, frame, audio):
        self.temp = temp
        self.frame = frame
        self.audio = audio
        self.face_detection()
        self.audio_detection()

    def face_detection(self):
        gray_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)       
        # print(gray_image.shape)
        # self.face = self.face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
        self.face = self.face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
        print("face detection = ", self.face)

    def audio_detection(self):
        amp = np.abs(self.audio.max() - self.audio.min())
        print(amp, self.audio.max(), self.audio.min())
        modAudio = self.audio * 1.2 /amp
        self.babyNoise = audioAssesment.classifyAudio(audioAssesment.offsetSample(modAudio))

    def is_face(self):
        if (self.face is not None):
            return (len(self.face) > 0)
        return False
        
    def temp_warning(self):
        return self.temp > 80
    
    def is_baby_cry(self):
        return self.babyNoise
    
    def notify(self):
        self.hazard = False
        if self.get_temp() > 20: 
            if self.is_face():
                self.hazard = True
                if self.is_baby_cry():
                    return "!!Hot,Cry,Face!"
                return "!!Hot and Face!"
            if self.is_baby_cry():
                self.hazard = True
                return "!!Hot and Cry!"
            self.hazard = False
            return "Hot Car no baby"
        return "temp is fine"




