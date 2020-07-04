# run until detect something
import websocket
import time
import requests
from post import post
import pygame
import mutagen.mp3
import tkinter as tk
from PIL import Image
from PIL import ImageTk
import os
import numpy as np
import queue
import threading
import tkinter as tk


# setting - set server ip / port
own_id = "..."
server = "ws://medistation.ljhnas.com:8080/" + own_id

# setting - http request
url = 'http://medistation.ljhnas.com/compare' # where to send


# socket connection
ws = websocket.WebSocket()
ws.connect(server)

# music setting
mp3 = mutagen.mp3.MP3(os.path.dirname(os.path.realpath(__file__)) +'/beep.mp3')
pygame.mixer.init(frequency=mp3.info.sample_rate)
pygame.mixer.music.load(os.path.dirname(os.path.realpath(__file__)) +'/beep.mp3')

while(True):

  text_file = open(os.path.dirname(os.path.realpath(__file__)) +'/wow.txt', "w")
  text_file.write('MediStation_monitor_main.png')
  text_file.close()

  while True:

      data = np.loadtxt(os.path.dirname(os.path.realpath(__file__)) +'/detected.txt', dtype = np.str)
      
      if data != "a":
        print("detected")
        pygame.mixer.music.play()
        time.sleep(0.2)
        mp3 = mutagen.mp3.MP3(os.path.dirname(os.path.realpath(__file__)) +'/nfc.mp3')
        pygame.mixer.init(frequency=mp3.info.sample_rate)
        pygame.mixer.music.load(os.path.dirname(os.path.realpath(__file__)) +'/nfc.mp3')
        pygame.mixer.music.play()

        start = time.time()
        # From now, wait for 5secs until the server to sends user's data(e-mail).
        # After 5 secs, restart this system.
        while (time.time() - start) < 10: # until time out
          e_mail = ws.recv()
          
          if e_mail != []:
            print(e_mail,e_mail,e_mail,)
            print("\n\n------------------------\nUser's e-mail has been arrived!\n------------------------\n\n")
            # send scanned data and own_id of this device to server
            '''
            response = post(data, e_mail, url)
            print(response)
            print(type(response))
            if response["eatable"]: # can take
              text_file = open(os.path.dirname(os.path.realpath(__file__)) +'/wow.txt', "w")
              text_file.write('MediStation_monitor_good.png')
              text_file.close()
            
            elif not response["eatable"]: # do not take
              text_file = open(os.path.dirname(os.path.realpath(__file__)) +'/wow.txt', "w")
              text_file.write('MediStation_monitor_bad.png')
              text_file.close()
            '''
            text_file = open(os.path.dirname(os.path.realpath(__file__)) +'/wow.txt', "w")
            text_file.write("MediStation_monitor_good.png")
            text_file.close()
            #break after 5 secs.
            time.sleep(5)
            break
      else:
        time.sleep(0.2)
        continue