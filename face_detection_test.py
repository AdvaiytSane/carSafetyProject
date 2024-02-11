import cv2
import matplotlib.pyplot as plt
from RiskAssessment import RiskAssessment
# define a video capture object
cap = cv2.VideoCapture(1)
temperature = 90

while (temperature > 80):
    ret, frame = cap.read()
    ass = RiskAssessment(81, frame)
    if ass.notify():
        print("baby detected and temperature above 80 degrees! Please check your car. ")
    else:
        print("baby not detected.")