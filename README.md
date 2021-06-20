# sources

- [General problem solution](https://towardsdatascience.com/a-table-detection-cell-recognition-and-text-extraction-algorithm-to-convert-tables-to-excel-files-902edcf289ec)
- [Morphological Operations used in computer vision (cv2 module)](https://docs.opencv.org/3.4/d4/d76/tutorial_js_morphological_ops.html)
- [VIDEO: Erosion and Dilation in Image Processing | morphological operations in image processing](https://www.youtube.com/watch?v=2LAooUu1IjQ&t=525s)

# screenshot-to-table
I can't take it anymore! This program will convert a screenshot of a table into a dataframe using computer vision (cv2) and optical character recognition (py-tesseract).

No matter how many times you ask, it just isn't enough.

The file 'screenshot to table demo.py' will demonstrate the image processing that is taking place in the program.  All of the file names for the test images are in the python code.  Just comment out all but one.

```python 3
# black all borders, odd formatting, row/col headers
# file = r'//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/complex.jpg'

# standard, black all borders format
file = r'//n0adcdata3/redirect$/nuajd15/My Documents/Python/image to table/all borders simple.jpg'
```

# Examples / Notes

## Import Image
Screenshot of an Excel file is uploaded as a gray scale image.  Each pixel will be read as a value between 0 and 255 (black to white).  In the next step, each pixel will have a value of either 0 or 255.  
![image](https://user-images.githubusercontent.com/47924318/120119075-b656d880-c163-11eb-9a6f-fce67ccb0af9.png)

## Threshold Image
Binary image where each pixel is either black or white depending on if it is greater or less than the threshold value. The threshold is automatically determined using Otsu's method which is an option of cv2.threshold().  If you're trying to find the best threshold value and there are two values where, one, the image is intensly white and the other, intensly black.  In that situation, Otsu's method will work well to find the optimal middle value.  Recall your personal experience with a photo copier because that's the kind of thing that's going on here, though in more complicated images like a photo copy (with shadowy gradients), the gaussian filter should be used.  Luckly in this case, we're just using simple screenshots.  
![image](https://user-images.githubusercontent.com/47924318/120119081-bc4cb980-c163-11eb-95ef-bcf3d33f4cb2.png)

## How Erosion and Dilution Works
Erosion of a matrix (A) given structuring element (B).  Lay the center-cell of B on top of each cell in A.  If all 1's in B match with 1's in A, then the center-cell of B is a 1 in the resulting image.  
![image](https://user-images.githubusercontent.com/47924318/122680649-46fe6280-d1be-11eb-83fe-12864f722896.png)  
Dilation is the opposite.  Overlay B on to each cell in A.  If at least one 1 in B matches with A, then the center-cell becomes a 1 in the resulting image.  
![image](https://user-images.githubusercontent.com/47924318/122680678-672e2180-d1be-11eb-94aa-27698ee88cfa.png)

## How Erosion is Used to Isolate Grid Lines
Erosion with a vertical kernel (structuring element), after multiple iterations, will anything that isn't horizontal and shorten any vertical lines.  
Dilation with the same vertical kernal is applied for the same number of iterations which will return the vertical lines to their original size.  
![image](https://user-images.githubusercontent.com/47924318/122683693-e166a200-d1ce-11eb-9815-9efc693451ae.png)  
![image](https://user-images.githubusercontent.com/47924318/122683806-a6b13980-d1cf-11eb-8af3-53dcef744c77.png)  
![image](https://user-images.githubusercontent.com/47924318/122683817-b2046500-d1cf-11eb-8834-1115ad79d3fc.png)  


