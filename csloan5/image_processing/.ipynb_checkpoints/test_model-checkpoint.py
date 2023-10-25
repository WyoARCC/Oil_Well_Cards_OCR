# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: tf_test
#     language: python
#     name: tf_test
# ---

# +
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os


# assign directory
directory = '/project/arcc-students/csloan5/OilWellCards_project/\
code/test_images/'
# This is just added to make the images be sorted alphabetically
file_list = os.listdir(directory)
#print(file_list)
file_list = sorted(file_list)
#print(file_list)
# -

alpha_num_dict = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',\
                  10:'A',11:'B',12:'C',13:'D',14:'E',15:'F',16:'G',17:'H',\
                  18:'I',19:'J',20:'K',21:'L',22:'M',23:'N',24:'O',25:'P',\
                  26:'Q',27:'R',28:'S',29:'T',30:'U',31:'V',32:'W',33:'X',\
                  34:'Y',35:'Z'}

# +
# load model
model = load_model("/project/arcc-students/csloan5/OilWellCards_project/\
code/models/CNN_OCR_model_1.h5")

# Create plot for all 36 numbers/letters
fig = plt.figure(figsize= (12, 12))
# iterate over files in test_images directory
count = 0
for filename in file_list:
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        ax = fig.add_subplot(6, 6, count+1)
        ax.set_xticks([]); ax.set_yticks([])
        count +=1
        
        img = cv2.imread(f)
        img_copy = img.copy()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (400,440))

        img_copy = cv2.GaussianBlur(img_copy, (7,7), 0)
        img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        _, img_thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)
        img_final = cv2.resize(img_thresh, (28,28))

        #img_final = cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB)
        img_final = np.reshape(img_final, (1,28,28,1))

        prediction = model.predict(img_final)

        img_pred = alpha_num_dict[np.argmax(prediction)]
        
        if(img_pred == '0'):
            img_pred = '0 (zero)'
        
        cv2.putText(img, img_pred, (20,420),\
                    cv2.FONT_HERSHEY_DUPLEX, 1.8, color = (255,0,30))
        
        ax.imshow(img)
# -


