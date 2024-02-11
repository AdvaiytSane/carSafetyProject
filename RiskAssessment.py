import cv2
class RiskAssessment:
    def __init__(self, temp, frame):
        self.temp = temp
        self.frame = frame

    def get_temp(self):
        return self.temp

    def get_raw_frame(self):
        return self.frame

    def is_face(self):
        gray_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        face = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
        return face!=()
    def temp_warning(self):
        return self.temp > 80
    def notify(self):
        return self.is_face() and self.temp_warning()