import cv2
import numpy as np
from tkinter import *

class getPath():
    def __init__(self,path):
        self.path=path
        self.record=False
        self.master= Tk()
        self.text=StringVar()
        self.e = Entry(self.master, textvariable=self.text)
        self.text.set(self.path)
        self.e.pack()
        self.e.focus_set()
        self.content=StringVar()
        
        self.b=Button(self.master, text="set", width=10, command=self.callback)
        self.b.pack() 
        
        
        
        mainloop()
    def callback(self):
        #print(self.e.get())
        self.path=self.e.get()
        self.master.destroy()
    def get(self):
        return self.path
    
    
#p=getPath()
#print(p.get())
class gui():
    def __init__(self):
        self.recording=False
        self.StartHover=False
        self.StartClick=False
        self.Startbbox=[(5,5),(95,95)]
        self.StopHover=False
        self.StopClick=False
        self.Stopbbox=[(105,5),(195,95)]

        self.font=cv2.FONT_HERSHEY_SIMPLEX
        self.path="/media/pi/SSD/saveVideoTest/video.avi"#"/home/pi/Desktop/video/video.mp4"
        self.pathbbox=[(5,105),(195,155)]
        self.PathHover=False
        self.PathClick=False
    def updateGUI(self):
        img=np.ones((200,200,3),np.uint8)*255
        if self.StartHover and not self.StartClick:
            Startcolor=(84,163,49)
        elif self.StartClick:
            Startcolor=(44,123,9)
        else:
            Startcolor=(104,183,89)
            
        if self.StopHover and not self.StopClick:
            Stopcolor=(84,163,49)
        elif self.StopClick:
            Stopcolor=(44,123,9)
        else:
            Stopcolor=(104,183,89)
        
        if self.PathHover and not self.PathClick:
            Pathcolor=(84,163,49)
        elif self.PathClick:
            Pathcolor=(44,123,9)
        else:
            Pathcolor=(104,183,89)
        
        cv2.rectangle(img, self.Startbbox[0], self.Startbbox[1], Startcolor, cv2.FILLED)
        img = cv2.putText(img, "Start", (self.Startbbox[0][0],self.Startbbox[0][1]+16), self.font, .5, (0,0,0), 1, cv2.LINE_AA)
        #cv2.rectangle(img, (Startbbox[0]+1,Startbbox[1]+1), (Startbbox[2]-1,Startbbox[3]-1), color, cv2.FILLED)
        cv2.rectangle(img, self.Stopbbox[0], self.Stopbbox[1], Stopcolor, cv2.FILLED)
        img = cv2.putText(img, "Stop", (self.Stopbbox[0][0],self.Stopbbox[0][1]+16), self.font, .5, (0,0,0), 1, cv2.LINE_AA)
        
        cv2.rectangle(img, self.pathbbox[0], self.pathbbox[1], Pathcolor, cv2.FILLED)
        #img = cv2.putText(img, "Stop", (self.Stopbbox[0][0],self.Stopbbox[0][1]+16), self.font, .5, (0,0,0), 1, cv2.LINE_AA)
        img = cv2.putText(img, "PATH: " +str(self.path), (5,135), self.font, .5, (0,0,0), 1, cv2.LINE_AA)
        return img

    def onmouse(self, event, x, y, flags, params):
        self.StartHover=False
        self.StopHover=False
        self.StartClick=False
        self.StopClick=False
        self.PathHover=False
        self.PathClick=False
        if x in range(self.Startbbox[0][0],self.Startbbox[1][0]) and y in range(self.Startbbox[0][1],self.Startbbox[1][1]):
            self.StartHover=True
            if event == cv2.EVENT_LBUTTONDOWN:
                self.StartClick=True
                self.recording=True

        if x in range(self.Stopbbox[0][0],self.Stopbbox[1][0]) and y in range(self.Stopbbox[0][1],self.Stopbbox[1][1]):
            self.StopHover=True
            if event == cv2.EVENT_LBUTTONDOWN:
                self.StopClick=True
                self.recording=False
        if self.recording==False:
            if x in range(self.pathbbox[0][0],self.pathbbox[1][0]) and y in range(self.pathbbox[0][1],self.pathbbox[1][1]):
                self.PathHover=True
                if event == cv2.EVENT_LBUTTONDOWN:
                    self.PathClick=True
                    p=getPath(self.path)
                    self.path=p.get()
    def getRecordingStatus(self):
        return self.recording
    def getPath(self):
        return self.path
    #updateGUI()
    

