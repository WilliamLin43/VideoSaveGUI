import cv2
import numpy as np
from threading import Thread
import time

class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self, resolution=(640,480), framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
            
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()
        '''
        self.out=None#=cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), framerate, resolution)
        self.recording=False
        self.resolution=resolution
        self.framerate=framerate
        self.path=path
        '''
        # Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
    # Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return
            '''
            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
            if self.recording:
                if not self.out == None:
                    self.out.write(self.frame)
                else:
                    print("start recording")
                    self.out=cv2.VideoWriter(self.path, cv2.VideoWriter_fourcc(*'mp4v'), self.framerate, self.resolution, True)
            else:
                if not self.out == None:
                    print("end recording")
                    self.out.release()
                    self.out=None
            '''
    def read(self):
    # Return the most recent frame
        return self.frame

    def stop(self):
    # Indicate that the camera and thread should be stopped
        self.stopped = True
    '''
    def recordupdate(self, status, path=""):
        self.recording=status
        self.path=path
    '''
        
        

class VideoSave:
    def __init__(self, path, FPS, dim):
        self.out=cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), FPS, dim)
        self.stopped = False
        self.newimg=False
        self.img=None
        self.FPS=FPS
    def start(self):
        Thread(target=self.update, args=()).start()
        return self
    def update(self):
        while True:
            now=time.time()
            
            if self.newimg:
                self.out.write(self.img)
                self.newimg=False

            #print("test")
            if self.stopped:
                self.out.release()
                return
            
            #cap fps
            timeDiff = time.time()-now
            if (timeDiff < 1.0/(self.FPS)):
                time.sleep(1/(self.FPS) - timeDiff)
    def stop(self):
        self.stopped = True
    def writeframe(self,img):
        self.img=img
        self.newimg=True

