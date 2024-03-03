import cv2

class RiskAssessment:
    def __init__(self, temp=None, frame=None):
        self.temp = temp
        self.frame = frame
        # self.face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # self.face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.face_classifier = cv2.CascadeClassifier('/home/advaiytsane/Downloads/haarcascade_frontalface_default.xml')
        self.face = None

    def get_temp(self):
        return self.temp

    def get_raw_frame(self):
        return self.frame
    
    def get_face(self):
        return self.face
    
    def update(self, temp = None, frame = None):
        self.temp = temp
        self.frame = frame
        gray_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)       
        # print(gray_image.shape)
        # self.face = self.face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
        self.face = self.face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    def is_face(self):
        return self.face!=()
    
    def temp_warning(self):
        return self.temp > 80
    
    def notify(self):
        return self.is_face() and self.temp_warning()