# Screenshot to table
# Andrew Davis personal project
# July 2021
### Bug: dilate and erode functionality are switched in cv2

from tkinter import *
from tkinter import filedialog
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
# computer vision
import cv2
# python imaging library
try:
    from PIL import Image
except ImportError:
    import Image
# Optical Character Recognition
# import pytesseract

# file = filedialog.askopenfilename()

#### TEST FILES ####

# file = r'//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/gradient.jpg'

# light-gray grid removed by threshold, has parentheses
# file = r'//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/small.jpg'

# light-gray grid, suggestion markers (text to number)
# file = r'//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/numbers as text with suggestion markers.jpg'

# black all borders, odd formatting, row/col headers
# file = r'//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/complex.jpg'

# standard, black all borders format
file = r'//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/all borders simple.jpg'

# PARAMETERS
# proportional size of kernel kernel_length= 1/kern_p
kern_p = 50
# used to erode and dilate pixels to get lines
vert_iter = 8
horz_iter = 8

# read file, flag=0 tells imread to return grayscale image
img = cv2.imread(file, 0)

# thresholding the image to a binary image
thresh, img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY |cv2.THRESH_OTSU)

# Length(width) of kernel as 100th of total width
kernel_len = np.array(img).shape[1]//kern_p
if kernel_len%2==0: kernel_len+=1

# Defining a vertical kernel to detect all vertical lines of image 
ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))

# Defining a horizontal kernel to detect all horizontal lines of image
hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))

# A kernel of 2x2
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

# get vertical lines
image_1 = cv2.dilate(img_bin, ver_kernel, iterations=vert_iter)
vertical_lines = cv2.erode(image_1, ver_kernel, iterations=vert_iter)
cv2.imwrite("//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/vertical.jpg", vertical_lines)

### Bug: dilate and erode functionality are switched in cv2
# Use horizontal kernel to detect and save the horizontal lines in a jpg
image_2 = cv2.dilate(img_bin, hor_kernel, iterations=horz_iter)
horizontal_lines = cv2.erode(image_2, hor_kernel, iterations=horz_iter)
cv2.imwrite("//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/horizontal.jpg",horizontal_lines)

# Combine horizontal and vertical lines in a new third image, with both having same weight.
grid = cv2.addWeighted(vertical_lines, 0.2, horizontal_lines, 0.2, 0.0)

thresh, grid = cv2.threshold(grid, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imwrite("//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/grid.jpg", grid)

bitxor = cv2.bitwise_xor(img_bin, grid)
bitnot = cv2.bitwise_not(bitxor)

# DEMO
figure, axis = plt.subplots(2,3)
axis[0,0].imshow(img_bin, cmap='gray')
axis[0,0].set_title('binary image')
axis[0,1].imshow(grid, cmap='gray')
axis[0,1].set_title('vert/horz combo')
axis[0,2].imshow(bitnot, cmap='gray')
axis[0,2].set_title('pixels not in grid')

# Detect contours for following box detection
contours, hierarchy = cv2.findContours(grid, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0
    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b:b[1][i], reverse=reverse))
    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)

# Sort all the contours by top to bottom.
contours, boundingBoxes = sort_contours(contours, method="top-to-bottom")

#Creating a list of heights for all detected boxes
heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]
#Get mean of heights
mean = np.mean(heights)

# Get position (x,y), width and height for every contour
box = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if (w<1000 and h<500):
        image = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        box.append([x,y,w,h])

axis[1,0].imshow(image,cmap='gray')
axis[1,0].set_title('boxes over image')



plt.show()

