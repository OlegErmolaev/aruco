import numpy as np
import cv2, PIL
from cv2 import aruco
from urllib import request
url = input()
d1 = 353.5533905932738
d2 = 250
def posAr(corners,i):
    x = int((corners[i][0][0][0] + corners[i][0][1][0] + corners[i][0][2][0] + corners[i][0][3][0]) / 4)
    y = int((corners[i][0][0][1] + corners[i][0][1][1] + corners[i][0][2][1] + corners[i][0][3][1]) / 4)
    return x,y
def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
    # return the image
    return image
    
#frame = cv2.imread('example_2.jpg')
frame = url_to_image(url)
fr = frame.copy()
cvtfr = cv2.inRange(fr,(0,0,150),(255,110,255))
cont, hierarchy = cv2.findContours(cvtfr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
c = max(cont, key=cv2.contourArea)
M = cv2.moments(c)
if(M['m00']!=0):
    cx = int(M['m10']/M['m00'])#координата центра по х
    cy = int(M['m01']/M['m00'])#координата центра по у

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_1000)
parameters =  aruco.DetectorParameters_create()
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
x,y = posAr(corners,0)
x1,y1 = posAr(corners,1)
d = ((x1-x)**2+(y1-y)**2)**0.5
if(len(ids)>3):
    scale = d2/d
else:
    scale = d1/d

dX = cx - x
dY = y - cy
print(str(int(dX*scale))+' '+str(int(dY*scale)))
    
    



