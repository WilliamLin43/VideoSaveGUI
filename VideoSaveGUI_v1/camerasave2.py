import cv2
import numpy as np
from threading import Thread
import time
import argparse
#from gui import onmouse, updateGUI
from gui import gui, getPath
from VideoStream import VideoStream#, VideoSave

parser = argparse.ArgumentParser()
parser.add_argument('--resolution', help='Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.',
                    default='1280x720')
parser.add_argument('--fps', help='Frames per second',
                    default=20)

args = parser.parse_args()
resW, resH = args.resolution.split('x')
w, h = int(resW), int(resH)
FPS = int(args.fps)

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()

# Initialize video stream
cv2.namedWindow("test",1)
g=gui()
cv2.setMouseCallback("test",g.onmouse)
path=g.getPath()
videostream = VideoStream(resolution=(w,h),framerate=FPS).start()
out=None
#videosave = None#VideoSave(path, FPS, (w,h)).start()

time.sleep(1)



while True:
    t1 = cv2.getTickCount()
    
    frame = videostream.read()
    #cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
    cv2.imshow('frame', frame)
    
    img=g.updateGUI()
    cv2.imshow("test",img)
    
    if g.getRecordingStatus():
        if out == None:
            #out=cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (w,h), True)
            #out=cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'MJPG'), FPS, (w,h), True)
            out=cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'WMV2'), 10, (w,h), True)
            print("recording start")
        out.write(frame)
    else:
        if not out == None:
            out.release()
            out=None
            print("recording stopped")
       
    
    '''
    if g.getRecordingStatus():
        path=g.getPath()
        videostream.recordupdate(True, path)
    else:
        videostream.recordupdate(False)
    '''
    '''
    if g.getRecordingStatus():
        if videosave==None:#videosave.getStatus():
            path=g.getPath()
            videosave = VideoSave(path, FPS, (w,h)).start()
            print("recording start")
        videosave.writeframe(img)
            
    else:
        if not videosave==None:#videosave.getStatus():
            videosave.stop()
            print("recording stop")
            videosave=None
    '''
    # Calculate framerate
    t2 = cv2.getTickCount()
    time1 = (t2-t1)/freq
    frame_rate_calc= 1/time1

    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
cv2.destroyAllWindows()
videostream.stop()
#if not videosave == None:
#    videosave.stop()