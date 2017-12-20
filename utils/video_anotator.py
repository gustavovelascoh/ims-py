'''
Created on Dec 19, 2017

@author: gustavo
'''
import numpy as np
import cv2


cap = cv2.VideoCapture("../possi/video.mp4")
frame_n = 0

try:

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame_n += 1
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Display the resulting frame
        cv2.imshow('frame',gray)
        
        #key_id = cv2.waitKey(0)
        #print(key_id)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except Exception:
    print("Exception!")
# When everything done, release the capture
print("Total frames: %d" % frame_n)
cap.release()
cv2.destroyAllWindows()