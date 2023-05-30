#AUTHOR: Yash Suresh , 2023

import tkinter as tk
import numpy as np
import time
import time

class Timer:
   
    def __init__(self,canvas):

        self.startTime = time.time()
        self.canvas = canvas
        self.canvas.create_text(70,70,text="Time Elapsed: 00:00 ",tags="timer")
        self.UpdateTimer()
        self.elapsedTime = 0


    def FormatTime(self, elapsedTime):
        mins = int(elapsedTime // 60)
        secs = int(elapsedTime % 60)
        str =  f"Time Elapsed: {mins:02d}:{secs:02d}"
        return str

    def UpdateTimer(self):
        self.elapsedTime = int(time.time() - self.startTime)
        self.canvas.itemconfigure("timer",text= self.FormatTime(self.elapsedTime))
        self.canvas.after(1000, self.UpdateTimer)