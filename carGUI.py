import tkinter as tk
import cv2
from tkinter import ttk
from PIL import Image, ImageTk
from picamera2 import Picamera2
import RPi.GPIO as gpio
import dht11
import lcd_1602
import RiskAssessment as RA

def update_temperature_humidity():
    # Simulated temperature and humidity values
    result = myDHT.read()
    if result.is_valid():
        temperature = result.temperature
        humidity = result.humidity
        print(f"Temperature: {temperature}�C\nHumidity: {humidity}%")
        TH_text.set(value=f"Temperature: {temperature}�C\nHumidity: {humidity}%")

    # temperature_label.config(text=f"Temperature: {temperature}�C\nHumidity: {humidity}%")
    temperature_label.after(100, update_temperature_humidity)

def update_video_frame():
    # _, frame = cap.read()
    frame =  piCam.capture_array()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)
    video_label.after(100, update_video_frame)

def update_baby_status():
    riskAss.update(frame = piCam.capture_array)
    isFace = riskAss.is_face()
 
    


lcd_1602.init(0x27, 1)
gpio.setmode(gpio.BCM)
myDHT = dht11.DHT11(pin = 17)

riskAss = RA()

piCam = Picamera2()
piCam.preview_configuration.main.size = (1280, 720)
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()  

root = tk.Tk()
root.title("Temperature, Humidity, and Video Display")

# Create labels for temperature/humidity and video frame
temperature = 25.5
humidity = 60.0
isFace = False
TH_text = tk.StringVar(value=f"Temperature: {temperature}�C\nHumidity: {humidity}%\nIs Face: {isFace}")

temperature_label = ttk.Label(root, font=("Helvetica", 12),textvariable=TH_text)
temperature_label.pack(side = tk.LEFT,ipadx=30, ipady=6)

video_label = ttk.Label(root)
video_label.pack(side = tk.RIGHT,ipadx=30, ipady=6)

# Start updating temperature/humidity and video frame
update_temperature_humidity()
update_video_frame()
update_baby_status()

root.mainloop()