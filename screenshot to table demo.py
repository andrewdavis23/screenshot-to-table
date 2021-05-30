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

# read file, flag=0 tells imread to return grayscale image
img = cv2.imread(file, 0)

# Plot original image
plt.imshow(img,cmap='gray')
plt.title('Screenshot')
plt.show()

# thresholding the image to a binary image
thresh,img_bin = cv2.threshold(img,0,255,cv2.THRESH_BINARY |cv2.THRESH_OTSU)

# Plot the binary image
plt.imshow(img_bin,cmap='gray')
plt.title('Binary Image. Otsu Optimized threshold = '+str(thresh))
plt.show()

# Length(width) of kernel as 100th of total width
kernel_len = np.array(img).shape[1]//100

# Defining a vertical kernel to detect all vertical lines of image 
ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))

# Defining a horizontal kernel to detect all horizontal lines of image
hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))

# A kernel of 2x2
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

##################
print("\nimage width\n",np.array(img).shape[1],"\nkernel length\n",kernel_len,"\nvertical kernel\n",ver_kernel,"\nhorizontal kernel\n",hor_kernel,"\nkernel\n",kernel)

# Use vertical kernel to detect and save the vertical lines in a jpg
# erosion, dilation used in sequence to remove noise
image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)
cv2.imwrite("//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/vertical.jpg", vertical_lines)

plt.imshow(image_1,cmap='gray')
plt.title('cv2.erode(img_bin, ver_kernel, iterations=3)')
plt.show()

plt.imshow(vertical_lines,cmap='gray')
plt.title('cv2.dilate(image_1, ver_kernel, iterations=3)')
plt.show()

###################
exit()

# Use horizontal kernel to detect and save the horizontal lines in a jpg
image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)
cv2.imwrite("//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/horizontal.jpg",horizontal_lines)

plt.imshow(horizontal_lines,cmap='gray')
plt.title('horizontal lines')
plt.show()

# Combine horizontal and vertical lines in a new third image, with both having same weight.
grid = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)

# Eroding and thesholding the image
grid = cv2.erode(~grid, kernel, iterations=2)

# Plot grid
plotting = plt.imshow(grid, cmap='gray')
plt.title('Combination of Vertical and Horizontal Pixels')
plt.show()

thresh, grid = cv2.threshold(grid,128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imwrite("//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/grid.jpg", grid)

bitxor = cv2.bitwise_xor(img_bin, grid)
bitnot = cv2.bitwise_not(bitxor)

# Plot binary image with grid exlcuded
plotting = plt.imshow(bitnot, cmap='gray')
plt.title('Binary Image with Grid Exlcuded')
plt.show()

