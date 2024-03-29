import cv2
import numpy as np
import time
from scipy.cluster import vq
import hues
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import argparse
import imutils
from matplotlib import pyplot as plt
from PIL import Image
from resizeimage import resizeimage

K=4

img=cv2.imread('C:/Users/Parinitha/Desktop/my project/kvasir-dataset/highly/img1.jpg',cv2.IMREAD_UNCHANGED)
print('original dime:',img.shape)
scale_percent=60
width=int(img.shape[1]*scale_percent/1000)
height=int(img.shape[0]*scale_percent/1000)
dim=(width,height)
resized=cv2.resize(img,dim,interpolation=cv2.INTER_AREA)
print('resizex dim:',resized.shape)
cv2.imshow("resized image",resized)

cv2.imshow('org img',img)
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow('gray',gray)

#img=cv2.imread('C:/Users/Parinitha/Desktop/my project/kvasir-dataset/img2.jpg',0)
gray=cv2.medianBlur(gray,5)

ret,th1=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
th2=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                          cv2.THRESH_BINARY,11,2)
th3=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                          cv2.THRESH_BINARY,11,2)
titles=['Original Image','Global Thresholding (v=127)','Adaptive Mean Thresholding','Adaptive Gaussian Thresholding']
images=[gray,th1,th2,th3]


for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

ret1,th1=cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

ret2,th2=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

blur=cv2.GaussianBlur(gray,(5,5),0)
ret3,th3=cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

images=[gray,0,th1,
         gray,0,th2,
         blur,0,th3]

titles=['Original Noisy Image','Histogram','Global Thresholding (v=127)',
        'Original Noisy Image','Histogram',"Otsu's Thresholding",
        'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]

for i in range(3):
    plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
    plt.title(titles[i*3]),plt.xticks([]),plt.yticks([])
    plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
    plt.title(titles[i*3+1]),plt.xticks([]),plt.yticks([])
    plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
    plt.title(titles[i*3+2]),plt.xticks([]),plt.yticks([])
plt.show()

kernel=np.ones((5,5),np.uint8)
erosion=cv2.erode(img,kernel,iterations = 1)
dilation=cv2.dilate(img,kernel,iterations =1)
cv2.imshow('hi',img)

cv2.imshow('li',erosion)

#img=cv2.imread('C:/Users/Parinitha/Desktop/my project/kvasir-dataset/img2.jpg')
cv2.imshow('gastestic',erosion)
frameYCrCb=cv2.cvtColor(erosion,cv2.COLOR_BGR2YCR_CB)
ch1,ch2,ch3=cv2.split(frameYCrCb)
ch1=cv2.equalizeHist(ch1)
cv2.imshow('ch1',ch1)
ch2=cv2.equalizeHist(ch2)
cv2.imshow('ch2',ch2)
ch3=cv2.equalizeHist(ch3)
cv2.imshow('ch3',ch3)
frameYCrCb=cv2.merge((ch1,ch2,ch3))
cv2.imshow('ycr',frameYCrCb)
frameHSV=cv2.cvtColor(erosion,cv2.COLOR_BGR2HSV)
cv2.imshow('HSV',frameHSV)
Z=erosion.reshape((-1,3))
Z=np.float32(Z)
criteria=(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,10,1.0)

K=10
ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
print(label)
print(center)

center=np.uint8(center)
res=center[label.flatten()]
res2=res.reshape((erosion.shape))

hsv= cv2.cvtColor(erosion,cv2.COLOR_BGR2HSV)
#cv2.imshow('hsv',hsv)
hue, saturation, value = cv2.split(hsv)
cv2.imshow('hue',hue)
cv2.imshow('value',value)
cv2.imshow('saturation',saturation)
cv2.imshow('res2',res2)



 
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
 
# construct the argument 
image = cv2.imread('C:/Users/Parinitha/Desktop/my project/kvasir-dataset/highly/img1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
 
# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
 
# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
 
# sort the contours from left-to-right and initialize the
# 'pixels per metric' calibration variable
(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = None
for c in cnts:
	# if the contour is not sufficiently large, ignore it
	if cv2.contourArea(c) < 100:
		continue
 
	# compute the rotated bounding box of the contour
	orig = image.copy()
	box = cv2.minAreaRect(c)
	box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
	box = np.array(box, dtype="int")
 
	# order the points in the contour such that they appear
	# in top-left, top-right, bottom-right, and bottom-left
	# order, then draw the outline of the rotated bounding
	# box
	box = perspective.order_points(box)
	cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
 
	# loop over the original points and draw them
	for (x, y) in box:
		cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
		(tl, tr, br, bl) = box
	(tltrX, tltrY) = midpoint(tl, tr)
	(blbrX, blbrY) = midpoint(bl, br)
 
	# compute the midpoint between the top-left and top-right points,
	# followed by the midpoint between the top-righ and bottom-right
	(tlblX, tlblY) = midpoint(tl, bl)
	(trbrX, trbrY) = midpoint(tr, br)
 
	# draw the midpoints on the image
	cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
 
	# draw lines between the midpoints
	cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
		(255, 0, 255), 2)
	cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
		(255, 0, 255), 2)

	# compute the Euclidean distance between the midpoints
	dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
	dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
 
	# if the pixels per metric has not been initialized, then
	# compute it as the ratio of pixels to supplied metric
	# (in this case, inches)
	if pixelsPerMetric is None:
		pixelsPerMetric = dB / 255
dimA = dA / pixelsPerMetric
dimB = dB / pixelsPerMetric
 
	# draw the object sizes on the image
cv2.putText(orig, "{:.1f}in".format(dimA),(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)
cv2.putText(orig, "{:.1f}in".format(dimB),(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)
 
	# show the output image
cv2.imshow("Image", orig)



cv2.waitKey()
cv2.destroyAllWindows()
