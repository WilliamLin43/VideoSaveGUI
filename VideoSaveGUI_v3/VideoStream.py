import cv2
import numpy as np
from threading import Thread
import time

class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,framerate=20):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        #ret = self.stream.set(3,resolution[0])
        #ret = self.stream.set(4,resolution[1])
        self.framerate=framerate
        self.resolution=None
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()
        
        self.out = None#cv2.VideoWriter(path+"/"+filename, cv2.VideoWriter_fourcc(*'XVID'), self.framerate, self.resolution)
    # Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
    # Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self
    
    def startRecording(self, path, filename, resolution):
        self.resolution=resolution
        self.out = cv2.VideoWriter(path+"/"+filename, cv2.VideoWriter_fourcc(*'XVID'), self.framerate, self.resolution)
    def stopRecording(self):
        self.out.release()
        self.out=None
        
    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                if not self.out==None:
                    self.out.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
            if not self.out==None:
                self.out.write(cv2.resize(self.frame, self.resolution))

                    

    def read(self):
        # Return the most recent frame
        return self.frame
        
    def stop(self):
    # Indicate that the camera and thread should be stopped
        self.stopped = True

