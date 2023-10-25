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
"""
 This script rotates any cards that are horizontal in their original pictures
 I have yet to figure out how to automate this
"""

import cv2
import numpy as np

imgPath = '/project/arcc-students/csloan5/OilWellCards_project/OilWellData/log_cards/'
outputDir = '/project/arcc-students/csloan5/OilWellCards_project/OilWellData/rotated_cards/'

# Rotate Eori_card_3b.jpg
img3b = cv2.imread(imgPath + 'Eori_card_3b.jpg')
assert img3b is not None
rotated = cv2.rotate(img3b, cv2.ROTATE_90_COUNTERCLOCKWISE)
cv2.imwrite(outputDir + 'Eori_card_3b_rotated.jpg', rotated)

# Rotate Eori_card_4b.jpg
img4b = cv2.imread(imgPath + 'Eori_card_4b.jpg')
assert img4b is not None
rotated = cv2.rotate(img4b, cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite(outputDir + 'Eori_card_4b_rotated.jpg', rotated)

# Rotate Eori_card_4c.jpg
img4c = cv2.imread(imgPath + 'Eori_card_4c.jpg')
assert img4c is not None
rotated = cv2.rotate(img4c, cv2.ROTATE_90_COUNTERCLOCKWISE)
cv2.imwrite(outputDir + 'Eori_card_4c_rotated.jpg', rotated)

# Rotate Eori_card_7a.jpg
img7a = cv2.imread(imgPath + 'Eori_card_7a.jpg')
assert img7a is not None
rotated = cv2.rotate(img7a, cv2.ROTATE_90_COUNTERCLOCKWISE)
cv2.imwrite(outputDir + 'Eori_card_7a_rotated.jpg', rotated)

# Rotate Eori_card_7b.jpg
img7b = cv2.imread(imgPath + 'Eori_card_7b.jpg')
assert img7b is not None
rotated = cv2.rotate(img7b, cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite(outputDir + 'Eori_card_7b_rotated.jpg', rotated)

# -


