# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: OCR_proj
#     language: python
#     name: ocr_proj
# ---

# +
import cv2
import numpy as np
import os
from deskew import determine_skew

rotateDirPath = '/project/arcc-students/csloan5/OilWellCards_project/\
OilWellData/rotated_cards/'
outputDir = '/project/arcc-students/csloan5/OilWellCards_project/OilWellData/\
processed_cards/'

"""
 This function grayscales the input image, then finds
 the skew angle using the deskew package, then uses 
 the angle to deskew the image, returning a rotated
 version of the image
 Some of this code was found on:
 https://pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
"""

def deskewImage(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
    angle = determine_skew(gray) # Find skew angle
    
    # Find center of image
    (h, w) = image.shape[:2] 
    center = (w // 2, h // 2)
    
    # Rotate the image
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskewed = cv2.warpAffine(image, M, (w, h),
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return deskewed


""" Loop over directory of rotated images """
for filename in os.listdir(rotateDirPath):
    file = rotateDirPath + filename
    if os.path.isfile(file): 

        # checking if it is a file
        img = None # Reset image first
        img = cv2.imread(file) # Read in image
        assert img is not None # Make sure that image was read in correctly

        # Normalizing the image first
        norm = cv2.normalize(img, None, 0, 200, cv2.NORM_MINMAX)
        
        # Deskew the image
        deskewed = deskewImage(norm)
        
        # Remove noise from the image
        denoised = cv2.fastNlMeansDenoisingColored(deskewed, None, 10, 10, 7, 15)
        
        # Thinning and Skeletonization
        kernel = np.ones((3,3),np.uint8)
        erosion = cv2.erode(denoised, kernel, iterations = 1)

        # Convert image to grayscale
        gray = cv2.cvtColor(denoised, cv2.COLOR_BGR2GRAY) 

        """
         Below are the many ways that I attempted thresholding the images. 
         Some ways were more effective than others

         Mean adaptive thresholding; Similar results to Gaussian adaptive
         thresholding but Gaussian seemed just slightly better in most tests.
        """
        # mean = cv2.adaptiveThreshold(norm,255,cv2.ADAPTIVE_THRESH_MEAN_C, \
        #                              cv2.THRESH_BINARY, 101, 45)

        """
         Gaussian adaptive thresholding; Seems to be the best choice for these
         images. I played around with the blockSize (5th arg) and constant 
         (6th arg) values, and found 101 and 30 to work pretty well.
        """
        gaus = cv2.adaptiveThreshold(gray, 255, \
                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 25)

        """
        Binary thresholding; resulting images were not great
        Tried playing with different parameter values, nothing really helped
        """
        #_,binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)


        """ Otsu Thresholding; Didn't seem to work well either """
        # _,otsu = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # # Otsu's thresholding after Gaussian filtering
        # blur = cv2.GaussianBlur(gray,(5,5),0)
        # _,otsuGaus = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        

        # Write the processed image
        cv2.imwrite(outputDir + filename[:12] + '_processed.jpg', gaus)

print("Done")
# -


