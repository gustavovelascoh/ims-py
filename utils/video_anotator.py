'''
Created on Dec 19, 2017

@author: gustavo
'''
import numpy as np
import cv2


square_points = []

def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "float32")
 
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[0]
    rect[2] = pts[2]
 
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[1]
    rect[3] = pts[3]
 
    # return the ordered coordinates
    return rect

def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    print(rect)
    (tl, tr, br, bl) = rect
 
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
 
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
 
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
 
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    print(rect, dst, M)
    
#     M = np.array([[  3.98331689e+00,   2.79923502e+01,  -9.36619674e+03],
#        [ -9.00519318e+00,   3.10852342e+01,  -7.19030040e+02],
#        [  7.37568334e-04,   2.93849985e-02,   1.00000000e+00]])
    
    M = np.array([[ -2.95982483e+00,  -2.67942037e+01,   6.32997485e+03],
       [  9.52838537e+00,  -2.26059344e+01,   1.61259929e+03],
       [ -9.52255725e-04,  -2.63745188e-02,   1.00000000e+00]])
    
    warped = cv2.warpPerspective(image, M, (maxWidth*2, maxHeight*2))
 
    # return the warped image
    return warped

def getPoint(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONUP:
        print("Selected point (%d,%d)" % (x,y))
        print("Save? [y] or n")
        key = cv2.waitKey(0)
        
        if key == ord('y'):
            if (len(square_points) <= 3):
                square_points.append((x,y))
                print(square_points)
                #cv2.circle(frame,(x,y),100,(255,0,0),-1)
    
    
frame = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',getPoint)
cap = cv2.VideoCapture("../possi/video.mp4")
frame_n = 0

try:

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame_n += 1
        # Our operations on the frame come here
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if (len(square_points) <= 3):
            for x,y in square_points:
                cv2.circle(frame,(x,y),5,(255,0,0),-1)
            # Display the resulting frame
            cv2.imshow('image',frame)
            print("f shape", np.shape(frame))
        else:
            pts = np.array(square_points, dtype = "float32")
            new_frame = four_point_transform(frame, pts)
            print("f shape", np.shape(new_frame))
            cv2.imshow('image', new_frame)
        
        
        key_id = cv2.waitKey(0)
        print(key_id)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except Exception as e:
    print("Exception!")
    print(e)
# When everything done, release the capture
print("Total frames: %d" % frame_n)
cap.release()
cv2.destroyAllWindows()