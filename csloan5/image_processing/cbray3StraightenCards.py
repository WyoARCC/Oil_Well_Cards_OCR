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
import numpy as np
from skimage import io
from skimage.color import rgb2gray
from skimage.transform import rotate

from deskew import determine_skew

# This function grayscales the input image, then finds
# the skew angle using the deskew package, then uses 
# the angle to deskew the image, returning a rotated
# version of the image
def deskewImage(imageInput):
    image = io.imread(imageInput)
    grayscale = rgb2gray(image)
    angle = determine_skew(grayscale)
    rotated = rotate(image, angle, resize=True) * 255
    return rotated.astype(np.uint8)

imageInput = "/project/arcc-students/csloan5/OilWellCards_project/OilWellData/rotated_cards/Eori_card_4c_rotated.jpg"

outputDir = "/project/arcc-students/csloan5/OilWellCards_project/OilWellData/unskewed_cards/Eori_card_4c_unskewed.jpg"

newImage = deskewImage(imageInput)

# This outputs the unskewed version of the image to a
# new location
io.imsave(outputDir, newImage)
# -


