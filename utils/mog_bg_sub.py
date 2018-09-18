'''
Created on Jun 15, 2018

@author: gustavo
'''

#####################################################################

# Example : perform GMM based foreground/background subtraction from a video file
# specified on the command line (e.g. python FILE.py video_file) or from an
# attached web camera

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2015 School of Engineering & Computing Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

#####################################################################

import cv2
import sys

#####################################################################

keep_processing = True;
camera_to_use = 1; # 0 if you have one camera, 1 or > 1 otherwise

#####################################################################

# define video capture object

cap = cv2.VideoCapture();

# check versions to work around this bug in OpenCV 3.1
# https://github.com/opencv/opencv/issues/6055

(major, minor, _) = cv2.__version__.split(".")
if ((major == '3') and (minor == '1')):
    cv2.ocl.setUseOpenCL(False);

# define display window name

windowName = "Live Camera Input"; # window name
windowNameBG = "Background Model"; # window name
windowNameFG = "Foreground Objects"; # window name
windowNameFGP = "Foreground Probabiity"; # window name

# if command line arguments are provided try to read video_name
# otherwise default to capture from attached H/W camera

if (((len(sys.argv) == 2) and (cap.open(str(sys.argv[1]))))
    or (cap.open(camera_to_use))):

    # create window by name (as resizable)

    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL);
    cv2.namedWindow(windowNameBG, cv2.WINDOW_NORMAL);
    cv2.namedWindow(windowNameFG, cv2.WINDOW_NORMAL);
    cv2.namedWindow(windowNameFGP, cv2.WINDOW_NORMAL);

    # create GMM background subtraction object (using default parameters - see manual)

    mog = cv2.createBackgroundSubtractorMOG2(history=4000, varThreshold=12, detectShadows=True);
    frame_cnt = 0
    while (keep_processing):
        frame_cnt += 1

        # if video file successfully open then read frame from video

        if (cap.isOpened):
            ret, frame = cap.read();

            # when we reach the end of the video (file) exit cleanly

            if (ret == 0):
                keep_processing = False;
                continue;

        # add current frame to background model and retrieve current foreground objects
        if frame_cnt != 1:
            fgmask = mog.apply(frame);
    
            # threshold this and clean it up using dilation with a elliptical mask
    
            fgthres = cv2.threshold(fgmask.copy(), 200, 255, cv2.THRESH_BINARY)[1];
            fgdilated = cv2.dilate(fgthres, kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)), iterations = 3);
    
            # get current background image (representative of current GMM model)
    
            bgmodel = mog.getBackgroundImage();
    
            # display images - input, background and original
    
            cv2.imshow(windowName,frame);
            cv2.imshow(windowNameFG,fgdilated);
            cv2.imshow(windowNameFGP,fgmask);
            cv2.imshow(windowNameBG, bgmodel);
    
            # start the event loop - essential
    
            # cv2.waitKey() is a keyboard binding function (argument is the time in milliseconds).
            # It waits for specified milliseconds for any keyboard event.
            # If you press any key in that time, the program continues.
            # If 0 is passed, it waits indefinitely for a key stroke.
            # (bitwise and with 0xFF to extract least significant byte of multi-byte response)
    
            key = cv2.waitKey(1) & 0xFF; # wait 40ms (i.e. 1000ms / 25 fps = 40 ms)
    
            # It can also be set to detect specific key strokes by recording which key is pressed
    
            # e.g. if user presses "x" then exit
    
            if (key == ord('x')):
                keep_processing = False;

    # close all windows

    cv2.destroyAllWindows()
    print(frame_cnt)
else:
    print("No video file specified or camera connected.");

#####################################################################
