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

# Defining a vertical kernel to detect all vertical lines of image 
ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))

# Defining a horizontal kernel to detect all horizontal lines of image
hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))

# A kernel of 2x2
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

# Kernal Stats
############## TEST ###################################################################
print("\nimage width\n",np.array(img).shape[1],"\nkernel length\n",kernel_len,"\nvertical kernel\n",ver_kernel,"\nhorizontal kernel\n",hor_kernel,"\nkernel\n",kernel)
########################################################################################

### Bug: dilate and erode functionality are switched in cv2
image_1 = cv2.dilate(img_bin, ver_kernel, iterations=vert_iter)
vertical_lines = cv2.erode(image_1, ver_kernel, iterations=vert_iter)
cv2.imwrite("//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/vertical.jpg", vertical_lines)

figure, axis = plt.subplots(2, 2)
# Plot original image
axis[0, 0].imshow(img,cmap='gray')
axis[0, 0].set_title('Screenshot')

# Plot the binary image
axis[0, 1].imshow(img_bin,cmap='gray')
axis[0, 1].set_title('Binary Image. Otsu Optimized threshold = '+str(thresh))

# Vertical erosion
axis[1, 0].imshow(image_1,cmap='gray')
axis[1, 0].set_title('cv2.erode(img_bin, ver_kernel, iterations={}) len(ver_kernel)={}'.format(vert_iter,len(ver_kernel)))

# Vertical dilation
axis[1, 1].imshow(vertical_lines,cmap='gray')
axis[1, 1].set_title('cv2.dilate(image_1, ver_kernel, iterations={})'.format(vert_iter))
plt.show()

### Bug: dilate and erode functionality are switched in cv2
# Use horizontal kernel to detect and save the horizontal lines in a jpg
image_2 = cv2.dilate(img_bin, hor_kernel, iterations=horz_iter)
horizontal_lines = cv2.erode(image_2, hor_kernel, iterations=horz_iter)
cv2.imwrite("//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/horizontal.jpg",horizontal_lines)

# Combine horizontal and vertical lines in a new third image, with both having same weight.
grid = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)

# GRID CREATION DEMO
figure, axis = plt.subplots(2, 2)
# Plot original image
axis[0, 0].imshow(vertical_lines,cmap='gray')
axis[0, 0].set_title('vertical lines')

axis[0, 1].imshow(horizontal_lines,cmap='gray')
axis[0, 1].set_title('horizontal lines')

axis[1, 0].imshow(grid,cmap='gray')
axis[1, 0].set_title('cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)')

# Eroding and thesholding the image
grid = cv2.erode(~grid, kernel, iterations=2)

axis[1, 1].imshow(vertical_lines,cmap='gray')
axis[1, 1].set_title('cv2.erode(~grid, kernel, iterations=2)')
plt.show()

# thresh, grid = cv2.threshold(grid, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# cv2.imwrite("//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/grid.jpg", grid)

bitxor = cv2.bitwise_xor(img_bin, grid)
bitnot = cv2.bitwise_not(bitxor)

# GRID LOGIC DEMO
figure, axis = plt.subplots(2, 2)
axis[0, 0].imshow(img_bin,cmap='gray')
axis[0, 0].set_title('Binary Image')

axis[0, 1].imshow(grid,cmap='gray')
axis[0, 1].set_title('Grid')

axis[1, 0].imshow(bitxor,cmap='gray')
axis[1, 0].set_title('cv2.bitwise_xor(img_bin, grid)')

axis[1, 1].imshow(bitnot,cmap='gray')
axis[1, 1].set_title('cv2.bitwise_not(bitxor)')

plt.show()

