import tkinter as tk
from PIL import Image
from PIL import ImageTk
from cv2 import cv2
import time
import os
import numpy as np
import threading
from scanner import scanner
import queue

window = tk.Tk()
window.title("MediStation")
window.geometry("1280x768")

class VideoCapture:
  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.cap.set(cv2.CAP_PROP_BUFFERSIZE,3)
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    self.q = queue.Queue()
     
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait() 
        except queue.Empty:
          pass
      self.q.put(frame)
      
  def read(self):
    return self.q.get()

capture = VideoCapture(0)


def detector():
    while True:
        frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        data = scanner(gray)
        
        if data != "nothing detected": # detected
            print(data)
            text_file = open(os.path.dirname(os.path.realpath(__file__)) +'/detected.txt', "w")
            text_file.write(data)
            text_file.close()

t = threading.Thread(target=detector,)
t.start()

label = tk.Label(window)
label.grid(row = 0, column = 0)

#Capture video frames
lmain = tk.Label(window)

def show_image():
    name = str(np.loadtxt(os.path.dirname(os.path.realpath(__file__)) + '/wow.txt', dtype=np.str))
    imgtk = tk.PhotoImage(file=os.path.dirname(os.path.realpath(__file__)) +"/"+name)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    label.after(20, show_image)

    if name == 'MediStation_monitor_main.png':
        lmain.place(x = 300, y = 270)

    else:
        lmain.place_forget()

def show_frame():
    frame = capture.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img   = Image.fromarray(cv2image).resize((720, 450))
    imgtk = ImageTk.PhotoImage(image = img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(20, show_frame)


show_image()
show_frame()
window.mainloop()