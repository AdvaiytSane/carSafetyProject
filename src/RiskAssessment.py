import cv2
import audioAssesment


class RiskAssessment:
    def __init__(self, temp=None, frame=None, audio=None):
        self.temp = temp
        self.frame = frame
        # self.face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # self.face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.face_classifier = cv2.CascadeClassifier('/home/advaiytsane/Downloads/haarcascade_frontalface_default.xml')
        self.face = None
        self.audio = audio
        self.babyNoise = None

    def get_temp(self):
        return self.temp

    def get_raw_frame(self):
        return self.frame
    
    def get_face(self):
        return self.face
    
    def update(self, temp = None, frame = None, audio=None):
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

    def audio_detection(self):
        self.babyNoise = audioAssesment.classifyAudio(audioAssesment.offsetSample(self.audio))

    def is_face(self):
        return self.face!=()
    
    def temp_warning(self):
        return self.temp > 80
    
    def is_baby_cry(self):
        return self.babyNoise
    
    def notify(self):
        if self.get_temp() > 20: 
            if self.is_face():
                if self.is_baby_cry():
                    return "Danger! Hot Car, Cry, Face detected!"
                return "Danger! Hot Car and Face detected!"
            
            if self.is_baby_cry():
                return "Danger! Hot Car and Cry detected!"
            return "Hot Car, no baby detected"
        return "temperature is moderate"
