#!/usr/bin/env python3
#coding=utf8

import sys
import pygame
from queue import Queue
import time
import socket
import threading
from io import BytesIO
import tkinter as tk


class GUI(tk.Frame):
  def __init__(self, master, queue, end_command):
    super().__init__(master)
    self.master = master
    self.queue = queue
    self.end_command = end_command
    
    self.pack()
    
    self.frame = tk.Frame(self, width=200, height=200)
    self.frame.pack()
    
    self.entry_token = tk.Entry(self.frame, show="*", width=60)
    self.entry_token.pack(side="top")
    
    self.btn_login = tk.Button(self.frame, text="Login", fg="white", bg="blue", command=self.btn_login_click)
    self.btn_login.pack(side="top")
    
    self.btn_exit = tk.Button(self.frame, text="Exit", fg="white", bg="red", command=self.btn_exit_click())
    self.btn_exit.pack(side="top")
  
  def btn_login_click(self):
    self.entry_token["state"] = "disabled"
    self.btn_login["state"] = "disabled"
    self.queue.put(True)
  
  def btn_exit_click(self):
    self.end_command()
    

class ThreadedClient:
  def __init__(self, master):
    self.master = master
    self.master.protocol("WM_DELETE_WINDOW", self.end_application)
    self.queue = Queue()
    self.gui = GUI(master, self.queue, self.end_application)
    
    self.running = True
    self.connected = False
    
    pygame.init()
    pygame.mixer.init()
    
    """sound_data = None
    with open("E:\\OneDrive\\Music\\Lord Darth Vader - Weird Al Yankovic Yoda.mp3", "rb") as yoda:
      sound_data = BytesIO(yoda.read())
    self.sound = pygame.mixer.Sound(sound_data)
    self.sound.set_volume(0.4)"""
    
    """self.thread1 = threading.Thread(target=self.workerThread1)
    self.thread1.start()"""
    
    self.thread1: threading.Thread = None
    
    self.socket: socket.socket = None
    self.sound: pygame.sound.Sound = None
    
    self.periodic_call()
  
  def end_application(self):
    self.running = False
    
    pygame.mixer.quit()
    pygame.quit()
  
  def periodic_call(self):
    if not self.running:
      sys.exit(1)
    
    if not self.connected and self.queue.qsize() > 0:
      try:
        self.socket = socket.socket()
        self.socket.connect(("3.122.99.185", 7450))
        self.socket.send(f"AUTH OVERLAY {self.gui.entry_token.get()}".encode())
        auth_msg: str = self.socket.recv(1024).decode().strip()
        if (auth_msg != "AUTH OK"):
          self.gui.entry_token["state"] = "normal"
          self.gui.btn_login["state"] = "normal"
          del self.socket
          self.socket = None
          self.queue.queue.clear()
        else:
          self.queue.queue.clear()
          self.connected = True
          self.thread1 = threading.Thread(target=self.workerThread1)
          self.thread1.start()
      except Exception as e:
        print(f"Exception: {e}")
        if self.socket is not None:
          del self.socket
        self.socket = None
        self.connected = False
        self.queue.queue.clear()
        self.gui.entry_token["state"] = "normal"
        self.gui.btn_login["state"] = "normal"
      self.master.after(50, self.periodic_call)
    elif self.connected and self.queue.qsize() > 0:
      sound_data = self.queue.get(0)
      sound_bytes = BytesIO(sound_data)
      if self.sound is not None:
        del self.sound
        self.sound = None
      self.sound = pygame.mixer.Sound(sound_bytes)
      self.sound.set_volume(0.3)
      sound_length = int(self.sound.get_length() * 1000)
      self.sound.play()
      self.master.after(sound_length + 2000, self.periodic_call)
    else:
      self.master.after(50, self.periodic_call)
  
  def workerThread1(self):
    while self.running:
      received_bytes: bytes = b""
      while received_bytes[-7:] != b"--END--":
        new_bytes = self.socket.recv(1024*1024)
        print(f"Received {len(new_bytes)} bytes")
        received_bytes += new_bytes
        print(f"All received bytes: {len(received_bytes)} bytes")
      print("Done receiving, time to play :-)")
      self.queue.put(received_bytes[:-7])
    self.socket.send("END")
    self.socket.close()
    self.socket = None

def main():
  root = tk.Tk()
  app = ThreadedClient(root)
  root.mainloop()
  return 0


if __name__ == "__main__":
  sys.exit(main())