import tkinter as tk
import cv2
from tkinter import ttk
from PIL import Image, ImageTk
import random
import sounddevice as sd

def update_temperature_humidity():
    # Simulated temperature and humidity values (update with real values)
    temperature = random.random()*5 + 20
    humidity = random.random()*5 + 60
    TH_text.set(value=f"Temperature: {temperature:3.1f}°C\nHumidity: {humidity:3.1f}%")
    # temperature_label.config(text=f"Temperature: {temperature}°C\nHumidity: {humidity}%")
    temperature_label.after(10000, update_temperature_humidity)

def update_video_frame():
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    # call image classifier here.
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)
    video_label.after(5000, update_video_frame)


def update_audio_classification():
    # Simulated audio-based classification output
    #record 10 seconds of video and call audio classifier
    

    is_baby_detected = (random.random() - 0.5) > 0.0
    if is_baby_detected:
        boolEvent = "Baby detected"
        detectedClass = "Baby Crying"
    else:
        boolEvent = "No Baby detected"
        detectedClass = "Noise"
    audio_class_text.set(value=f"{boolEvent}\ndetectedClass: {detectedClass}")
    audio_classification_label.after(5000, update_audio_classification)

def textParentCell():
    print("texting parent")
    pass

def informParent():
    if badCounter > 10:
        textParentCell()

def warningSign(t, a, c):
    if (t > 30) and a and c:
        return 3
    elif (t > 30) and a:
        return 2
    elif (t > 30) and c:
        return 2
    elif (a):
        return 1 # baby is crying but temp is ok.
    else:
        return 0

def update_bad_counter():
    incr = warningSign(temperature, audioEvent, cameraEvent)
    if incr > 0:
        badCounter += incr # increment counter
    else:
        badCounter = 0 #reset counter

root = tk.Tk()
root.configure(bg='blue')
root.title("Temperature, Humidity, and Video Display")

# Simulated video capture (replace with actual camera/video source)
cap = cv2.VideoCapture(0)

audioEvent = False
cameraEvent = False
badCounter = 0

# Create labels for temperature/humidity and video frame
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

# Start updating temperature/humidity and video frame
update_temperature_humidity()
update_video_frame()
update_audio_classification()
update_bad_counter()

root.mainloop()