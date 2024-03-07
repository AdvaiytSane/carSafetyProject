# GUI libs
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
#Camera libs
import cv2
from picamera2 import Picamera2
#Temp libs
import RPi.GPIO as gpio
import dht11
#LC libs
import lcd_1602 as lcd_1602
# Audio libs
import sounddevice as sd
import time
import requests

# main project class 
from RiskAssessment import RiskAssessment
import audioAssesment

def update_temperature_humidity():
    # Simulated temperature and humidity values (update with real values)
    TH_text.set(value=f"Temperature: {temperature:3.1f}°C\nHumidity: {humidity:3.1f}% \n Time: {time.time()}")
    temperature_label.after(10000, update_temperature_humidity)

def update_video_frame():
    frame = riskAss.get_raw_frame()
    # if faces are detected, then add bounding boxes
    if riskAss.is_face():
        face_locations = riskAss.get_face()
        for x, y, w, h  in face_locations:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        

    # Update GUI
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)
    video_label.after(5000, update_video_frame)


def update_audio_classification():
    # Simulated audio-based classification output
    if riskAss.is_baby_cry():
        audio_class_text.set(value=f"Crying baby detected")
    else:
        audio_class_text.set(value=f"No crying detected in audio")
    audio_classification_label.after(5000, update_audio_classification)

def update_hazard_classification():
    #record 10 seconds of video and call audio classifier
    process_status_label.set(value="Audio: Recording")
    audioSample = audioAssesment.recordSample()

    process_status_label.set(value="Camera: capture")
    frame = piCam.capture_array()
    process_status_label.set(value="Audio, Camera: Standby")

    process_status_label.set(value="Reading Temperature")
    result = myDHT.read()
    if result.is_valid():
        temperature = result.temperature
        humidity = result.humidity
        lcd_1602.write(0,0, "Temp is {0}".format(temperature))
    
    process_status_label.set(value="Risk assement sensor update")

    riskAss.update(temperature, frame, audioSample)
    message = riskAss.notify()
    if riskAss.hazard:
        textParentCell(message)
        process_status_label.set(value="Sent notification to guarandian")
    else:
        process_status_label.set(value="Standby")
    hazard_classification_label.after(5000, update_hazard_classification)


def textParentCell(message):
    PARENT_PHONE = '6692514210'
    warnText = f"texting {PARENT_PHONE}: {message}"
    print(warnText)
    process_status_label.set(value=warnText)
    if False:
        resp = requests.post('https://textbelt.com/text', {
                        'phone': PARENT_PHONE,
                        'message': message,
                        'key': 'af71119ada56b527242e3f862f3e4e400817350bO0eyayo2OU1Ljs7Ums3bWbmvd',
                        })

root = tk.Tk()
root.configure(bg='blue')
root.title("SaveASmile")

# initialize lcd and sensors
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

# Simulated video capture (replace with actual camera/video source)
cap = cv2.VideoCapture(0)


# Create labels for temperature/humidity, audio and video frame
temperature = 25.5
humidity = 60.0
TH_text = tk.StringVar(value=f"Temperature: {temperature:3.1f}°C\nHumidity: {humidity:3.1f}%")
temperature_label = ttk.Label(root, font=("Helvetica", 12),textvariable=TH_text)
temperature_label.pack(side = tk.LEFT,ipadx=30, ipady=6)

audio_class_text = tk.StringVar(value="No Baby detected\nNoise")
audio_classification_label = ttk.Label(root, font=("Helvetica", 12),textvariable=audio_class_text)
audio_classification_label.pack()

video_label = ttk.Label(root)
video_label.pack(side = tk.RIGHT,ipadx=30, ipady=6)

# Main detection and classification process
process_status_label = tk.StringVar(value="Process: Standby")
hazard_classification_label = ttk.Label(root, font=("Helvetica", 12),textvariable=process_status_label)
hazard_classification_label.pack()

# Start updating temperature/humidity and video frame
update_temperature_humidity()
update_video_frame()
update_audio_classification()
update_hazard_classification()

root.mainloop()