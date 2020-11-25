import pygame
import tkinter
from tkinter import filedialog
import os
from VideoStream import VideoStream
import cv2

from os import listdir
from os.path import isfile, join

def getfiles(path, name):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    count=0
    for f in files:
        if name in f:
            count+=1
    return count

def checkmousebox(box,mouse):
        if (box[0]+box[2]>mouse[0]>box[0] 
            and box[1]+box[3]>mouse[1]>box[1]):
            return True
        return False
    
class SSbuttons:
    def __init__(self, world):
        self.world=world
        self.recordbox=[15,15,150,100]
        self.recording=False
        
        
        self.autoIncrement=False
        self.autoIncrementbox=[180,60,10,10]
        self.autoIncrementnum=0
        
        self.filepathbox=[180,80,75,20]
        self.filepath=os.getcwd()
        
        self.filenamebox=[180,30,100,20]
        self.filename=["v","i","d","e","o"]
        
        self.resolutions=[(1920,1080),(1080,960),(720,480),(640,480),(300,300)]
        self.resolutionselect=3
        self.resolutionColumnHeight=5
        self.resolutionlocation=(15,145)
        
        self.flipped=[False]*5
        self.fliprotation=["flip X","flip Y",cv2.ROTATE_90_CLOCKWISE,cv2.ROTATE_180,cv2.ROTATE_90_COUNTERCLOCKWISE]
        self.fliprotationtext=["flip X","flip Y",90,180,270]
        self.flipposition=(250,145)

        self.videostream=VideoStream(self).start()
        self.image=None
        
    def stop(self):
        self.videostream.stop()
        cv2.destroyAllWindows()
        
    def update(self):
        for key in self.world.keyspress:
            if key == pygame.K_BACKSPACE:
                self.filename = self.filename[0:-1]
            elif key <= 127:
                self.filename.append(chr(key))
        
                
        
        if self.world.running:
            if self.videostream.grabbed:
                cv2.imshow("test",self.image)
                #self.videostream.grabbed=False
        else:
            cv2.destroyAllWindows()

    def draw(self):
        #rotations and flips
        self.world.screen.blit(self.world.fontobject.render("Rotations", 1, (0,0,0)),(self.flipposition,self.flipposition))
        for i in range(len(self.flipped)):
            xx = self.flipposition[0]
            yy = self.flipposition[1]+i*20+15
            box=[xx,yy,10,10]
            if checkmousebox(box,(self.world.mouse_x,self.world.mouse_y)):
                if self.flipped[i]:
                    color=(10,150,10)
                else:
                    color=(150,150,150)
                    
                if self.world.mouse_left_down:
                    self.flipped[i]=not self.flipped[i]
                    self.videostream.flipped=self.flipped
            else:
                if self.flipped[i]:
                    color=(10,200,10)
                else:
                    color=(200,200,200)
            pygame.draw.rect(self.world.screen, (0,0,0),
                (box[0],box[1],
                 box[2],box[3]), 0)
            pygame.draw.rect(self.world.screen, color,
                (box[0]+1,box[1]+1,
                 box[2]-1,box[3]-1), 0)
            self.world.screen.blit(self.world.fontobject.render(str(self.fliprotationtext[i]), 1, (0,0,0)),(box[0]+12,box[1]))
        
        #resolutions
        self.world.screen.blit(self.world.fontobject.render("Resolutions", 1, (0,0,0)),self.resolutionlocation)
        for i in range(len(self.resolutions)):
            xx = self.resolutionlocation[0] + divmod(i,self.resolutionColumnHeight)[0]*100
            yy = self.resolutionlocation[1]+ 15 + divmod(i,self.resolutionColumnHeight)[1]*25
            box=[xx,yy,100,20]
            if checkmousebox(box,(self.world.mouse_x,self.world.mouse_y)):
                color=(150,150,150)
                if self.world.mouse_left_down:
                    self.resolutionselect=i
                if self.resolutionselect==i:
                    color=(0,200,200)
            else:
                if self.resolutionselect==i:
                    color=(0,255,255)
                else:
                    color=(200,200,200)
            pygame.draw.rect(self.world.screen, (0,0,0),
                (box[0],box[1],
                 box[2],box[3]), 0)
            pygame.draw.rect(self.world.screen, color,
                (box[0]+1,box[1]+1,
                 box[2]-1,box[3]-1), 0)
            self.world.screen.blit(self.world.fontobject.render(str(self.resolutions[i]), 1, (0,0,0)),(box[0]+3,box[1]+3))
        
        #file name
        self.world.screen.blit(self.world.fontobject.render("File settings", 1, (0,0,0)),(self.filenamebox[0],self.filenamebox[1]-15))
        
        pygame.draw.rect(self.world.screen, (0,0,0),
                (self.filenamebox[0],self.filenamebox[1],
                 self.filenamebox[2],self.filenamebox[3]), 0)
        pygame.draw.rect(self.world.screen, (200,200,200),
                (self.filenamebox[0]+1,self.filenamebox[1]+1,
                 self.filenamebox[2]-1,self.filenamebox[3]-1), 0)
        self.world.screen.blit(self.world.fontobject.render(str.join("",self.filename), 1, (0,0,0)),(self.filenamebox[0]+3,self.filenamebox[1]+3))
        self.world.screen.blit(self.world.fontobject.render(".avi", 1, (0,0,0)),(self.filenamebox[0]+self.filenamebox[2]+3,self.filenamebox[1]+3))
        
        #file path
        if checkmousebox(self.filepathbox,(self.world.mouse_x,self.world.mouse_y)):
            color=(150,150,150)
            if self.world.mouse_left_down:
                root = tkinter.Tk()
                root.withdraw()
                currdir = os.getcwd()
                self.filepath = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
                
        else:
            color=(200,200,200)
            
        pygame.draw.rect(self.world.screen, (0,0,0),
                (self.filepathbox[0],self.filepathbox[1],
                 self.filepathbox[2],self.filepathbox[3]), 0)
        pygame.draw.rect(self.world.screen, color,
                (self.filepathbox[0]+1,self.filepathbox[1]+1,
                 self.filepathbox[2]-1,self.filepathbox[3]-1), 0)
        self.world.screen.blit(self.world.fontobject.render("select folder", 1, (0,0,0)),(self.filepathbox[0]+2,self.filepathbox[1]+self.filepathbox[3]/3))
        self.world.screen.blit(self.world.fontobject.render("folder: "+str(self.filepath), 1, (0,0,0)),(self.filepathbox[0]+2,self.filepathbox[1]+self.filepathbox[3]+5))
        
        #auto increment
        if checkmousebox(self.autoIncrementbox,(self.world.mouse_x,self.world.mouse_y)):
            if self.autoIncrement:
                color=(10,150,10)
            else:
                color=(150,150,150)
                
            if self.world.mouse_left_down:
                self.autoIncrement=not self.autoIncrement
        else:
            if self.autoIncrement:
                color=(10,200,10)
            else:
                color=(200,200,200)
            
        pygame.draw.rect(self.world.screen, (0,0,0),
                (self.autoIncrementbox[0],self.autoIncrementbox[1],
                 self.autoIncrementbox[2],self.autoIncrementbox[3]), 0)
        pygame.draw.rect(self.world.screen, color,
                (self.autoIncrementbox[0]+1,self.autoIncrementbox[1]+1,
                 self.autoIncrementbox[2]-1,self.autoIncrementbox[3]-1), 0)
        self.world.screen.blit(self.world.fontobject.render("auto increment file names", 1, (0,0,0)),(self.autoIncrementbox[0]+self.autoIncrementbox[2]+10,self.autoIncrementbox[1]))
        
        
        #stop/start recording
        if checkmousebox(self.recordbox,(self.world.mouse_x,self.world.mouse_y)):
            if self.recording:
                color=(10,200,10)
            else:
                color=(200,200,200)
            if self.world.mouse_left_down:
                if self.recording:
                    #stop
                    self.recording=False
                    self.videostream.stopRecording()
                    #self.videostream=None
                else:
                    #start
                    if not self.filepath=="" and not len(self.filename)==0:
                        self.recording=True
                        if self.autoIncrement:
                            self.autoIncrementnum=getfiles(self.filepath, str.join("",self.filename))
                            fname=str.join("",self.filename)+str(self.autoIncrementnum)+".avi"
                        else:
                            fname=str.join("",self.filename)+".avi"
                        
                        self.videostream.startRecording(self.filepath, fname,self.resolutions[self.resolutionselect])#VideoStream(, ).start()
                        #print(self.resolutions[self.resolutionselect])
                        
        else:
            if self.recording:
                color=(10,255,10)
            else:
                color=(150,150,150)
            
        pygame.draw.rect(self.world.screen, (0,0,0),
                (self.recordbox[0],self.recordbox[1],
                 self.recordbox[2]+1,self.recordbox[3]+1), 0)
        pygame.draw.rect(self.world.screen, color,
                (self.recordbox[0]+1,self.recordbox[1]+1,
                 self.recordbox[2]-1,self.recordbox[3]-1), 0)
        
        if self.recording:
            self.world.screen.blit(self.world.fontobject.render("stop recording", 1, (0,0,0)),(self.recordbox[0]+self.recordbox[2]/2-50,self.recordbox[1]+self.recordbox[3]/2))
        else:
            self.world.screen.blit(self.world.fontobject.render("start recording", 1, (0,0,0)),(self.recordbox[0]+self.recordbox[2]/2-50,self.recordbox[1]+self.recordbox[3]/2))
            