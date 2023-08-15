#this script is meant to clean, crop, and convert all images to text.
#it uses cv2 to clean and crop the image and pytesseract to perform OCR on the images
#large parts of code taken from https://pyimagesearch.com/2021/11/22/improving-ocr-results-with-basic-image-processing/

#written by Collin Dixon



from turtle import left, right
import numpy as np
import pytesseract
import argparse
import imutils
import cv2
from pdf2image import convert_from_path
import os
import sys








def ocr_core(file_name_here,psm):
    sconfig='--psm '+str(psm)
    try:
        text = pytesseract.image_to_string(file_name_here,
        config=sconfig)
    except:
        text='failed'
    return text

def ocr_core_tsv(image):
    try:
        text=pytesseract.image_to_data(image)
    except:
        text='--FAILED--'
    return text
    

#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#	help="path to image")g 
#args = vars(ap.parse_args())

#cleans  single image and outputs the cleaned image
def cleanupImage(image):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # threshold the image using Otsu's thresholding method
    thresh = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # apply a distance transform which calculates the distance to the
    # closest zero pixel for each pixel in the input image
    dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)

    # normalize the distance transform such that the distances lie in
    # the range [0, 1] and then convert the distance transform back to
    # an unsigned 8-bit integer in the range [0, 255]
    dist = cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
    dist = (dist * 255).astype("uint8")


    # threshold the distance transform using Otsu's method
    dist = cv2.threshold(dist, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/distotsu.jpg", dist)

    # apply an "opening" morphological operation to disconnect components
    # in the image
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
    opening = cv2.morphologyEx(dist, cv2.MORPH_OPEN, kernel)
    #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/opening.jpg", opening)

    # find contours in the opening image, then initialize the list of
    # contours which belong to actual characters that we will be OCR'ing
    cnts = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    chars = []
    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(c)
        # check if contour is at least 35px wide and 100px tall, and if
        # so, consider the contour a digit
        if w >= 5 and h >= 5:
            chars.append(c)

    # compute the convex hull of the characters
    chars = np.vstack([chars[i] for i in range(0, len(chars))])
    hull = cv2.convexHull(chars)
    # allocate memory for the convex hull mask, draw the convex hull on
    # the image, and then enlarge it via a dilation
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.drawContours(mask, [hull], -1, 255, -1)
    mask = cv2.dilate(mask, None, iterations=2)
    #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/mask.jpg", mask)
    # take the bitwise of the opening image and the mask to reveal *just*
    # the characters in the image
    final = cv2.bitwise_and(opening, opening, mask=mask)
    #filenumber=file.split(".")[0]
    
    return final

#this function operates on a directory to clean the images in that directory and save them in outputPath. It returns the directory containing coverted images
def cleanup(directory,outputPath):
    #create the output directory
    completeOutputPath=os.path.join(outputPath,directory.split('/')[-1])
    os.makedirs(completeOutputPath, exist_ok=True)

    #create a list of failed files
    failedfiles=[]
    
    for file in  os.listdir(directory):
        #the mighty try statement
        try:
            pdfimage=directory+'/'+file
            image=convert_from_path(pdfimage)
            image[0].save(os.path.join(outputPath,'temp',file+'.jpg'),'jpeg')
            image=cv2.imread(os.path.join(outputPath,'temp',file+'.jpg'))
         
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # threshold the image using Otsu's thresholding method
            thresh = cv2.threshold(gray, 0, 255,
                cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            # apply a distance transform which calculates the distance to the
            # closest zero pixel for each pixel in the input image
            dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)

            # normalize the distance transform such that the distances lie in
            # the range [0, 1] and then convert the distance transform back to
            # an unsigned 8-bit integer in the range [0, 255]
            dist = cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
            dist = (dist * 255).astype("uint8")
    

            # threshold the distance transform using Otsu's method
            dist = cv2.threshold(dist, 0, 255,
                cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/distotsu.jpg", dist)

            # apply an "opening" morphological operation to disconnect components
            # in the image
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
            opening = cv2.morphologyEx(dist, cv2.MORPH_OPEN, kernel)
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/opening.jpg", opening)

            # find contours in the opening image, then initialize the list of
            # contours which belong to actual characters that we will be OCR'ing
            cnts = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            chars = []
            # loop over the contours
            for c in cnts:
                # compute the bounding box of the contour
                (x, y, w, h) = cv2.boundingRect(c)
                # check if contour is at least 35px wide and 100px tall, and if
                # so, consider the contour a digit
                if w >= 5 and h >= 5:
                    chars.append(c)

            # compute the convex hull of the characters
            chars = np.vstack([chars[i] for i in range(0, len(chars))])
            hull = cv2.convexHull(chars)
            # allocate memory for the convex hull mask, draw the convex hull on
            # the image, and then enlarge it via a dilation
            mask = np.zeros(image.shape[:2], dtype="uint8")
            cv2.drawContours(mask, [hull], -1, 255, -1)
            mask = cv2.dilate(mask, None, iterations=2)
            #cv2.imwrite("/project/arcc-students/cdixon15/radiocarbon_project/mask.jpg", mask)
            # take the bitwise of the opening image and the mask to reveal *just*
            # the characters in the image
            final = cv2.bitwise_and(opening, opening, mask=mask)
            #filenumber=file.split(".")[0]
            
            cv2.imwrite(os.path.join(completeOutputPath,str(file)+".jpg"), final)
        except:
            failedfiles.append(str(file))
    
    print("These files failed cleanup: ",failedfiles)
    return completeOutputPath
            
#takes a directory and outputpath, translates images in directory to txt, and places the txt files in outputpath
def ocrOnDirectory(directory,outputPath):
    #create the output directory
    completeOutputPath=os.path.join(outputPath,directory.split('/')[-1])
    os.makedirs(completeOutputPath, exist_ok=True)
    #create a list of failed files
    failedfiles=[]
    for file in  os.listdir(directory):
        
        
        text=ocr_core(convert_from_path(os.path.join(directory,str(file)))[0], 3)
        

        output_writer = open(os.path.join(completeOutputPath,str(file)+'.txt'), "w")
        output_writer.write(text)
    print("These files failed OCR: ",failedfiles)

#With cleaning
def tsv_ocrOnDirectory(directory,outputPath):
    print('ran with outputPath ',outputPath)
    for file in os.listdir(directory):
        filePath=os.path.join(directory,file)
        if os.path.isdir(filePath):
            newInput=os.path.join(directory,file)
            newOutput=os.path.join(outputPath,file)
            os.makedirs(newOutput, exist_ok=True)
            print('directory, ',newOutput, 'created')
            print('new inputs are, ', newInput," ",newOutput)
            tsv_ocrOnDirectory(newInput,newOutput)
        if os.path.isfile(filePath):
            print('file is ', filePath)
            try:
                image=cleanupImage(np.array(convert_from_path(filePath)[0]))
                text=ocr_core_tsv(image)
                ##print(text)
                ##print('new')
                output_writer = open(os.path.join(outputPath,str(file)+'.tsv'), "w")
                output_writer.write(text)
                print(file, 'OCR written to ',os.path.join(outputPath,str(file)+'.tsv'))
            except:
                print(filePath, ' failed')

    return 

#takes a path to an image and outputs an example of each PSM setting to the destination folder
def testAllPSM(pathToImage,destination):
    for i in range(1,14):
        print(i)
        text=ocr_core(pathToImage, i)
        output_writer = open(os.path.join(destination,str(pathToImage)+'_'+str(i)+'.txt'), "w")
        output_writer.write(text)
#BAD Function?
#I marked this as bad for some reason but it seems to work fine
def convertAllOilCards(destination):
    for folder in  os.listdir('/project/arcc-students/enhanced_oil_recovery_cards'):
        os.makedirs(os.path.join(destination,folder), exist_ok=True)
        for folder2 in os.listdir(os.path.join('/project/arcc-students/enhanced_oil_recovery_cards',folder)):            
            ocrOnDirectory(os.path.join('/project/arcc-students/enhanced_oil_recovery_cards',folder,folder2),os.path.join(destination,folder))

#TODO
#DO NOT USE
#takes an image and section and performs OCR on only the specified section
def ocrOnSection(image,section):    

    img_cv = cv2.imread(r'/<path_to_image>/digits.png')

    # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
    # we need to convert from BGR to RGB format/mode:
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    print(pytesseract.image_to_string(img_rgb))
    # OR
    img_rgb = Image.frombytes('RGB', img_cv.shape[:2], img_cv, 'raw', 'BGR', 0, 0)
    print(pytesseract.image_to_string(img_rgb))

'''
#takes an image of type 1, outputs text file using customized OCR process from layoutDetection
def typeOneOCR(image):   
    
    linesV=lineDetection.findLines(image,-.78,.78)
    linesV=lineDetection.getBestTwoLines(linesV)
    linesH=lineDetection.findLines(image,.78, 2.35)
    linesH=lineDetection.getBestLine(linesH)    

    topImage,leftImage,centerImage,rightImage=lineDetection.splitImage(image,linesH,linesV)

    textTop=ocr_core(topImage, 3)
    textLeft=ocr_core(leftImage, 3)
    textCenter=ocr_core(centerImage, 3)
    textRight=ocr_core(rightImage, 3)

    #the section labels may need to be replaced to make sure they are unique from raw OCR output and easy to parse
    textFull="--SECTIONLABELTOP: "+os.linesep+textTop+os.linesep+ \
            "--SECTIONLABELLEFT: "+os.linesep+textLeft+os.linesep+ \
            "--SECTIONLABELCENTER: "+os.linesep+textCenter+os.linesep+ \
            "--SECTIONLABELRIGHT: "+os.linesep+textRight

    
    return textFull
'''
def main():
    print('start')
    #do all the main stuff

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True,
    	help="path to input directory") 
    ap.add_argument("-c", "--cleaned", required=False,
        help="path to directory of cleaned images") 
    ap.add_argument("-o", "--output", required=True,
        help="path to directory of text files") 
    args = vars(ap.parse_args())
    
    #testAllPSM('/project/arcc-students/cdixon15/oilCardProject/typedOCR/cleaned/temp/310-0000.pdf.jpg','/project/arcc-students/cdixon15/oilCardProject/typedOCR/PSMTest')
    #cleanupOutput=cleanup(args['input'],args['cleaned'])
    #ocrOnDirectory(cleanupOutput,args['output'])
    #convertAllOilCards(args['output'])
    #image=layoutDetection.lineDetection.firstPageToImage(args['input'])
    #text=typeOneOCR(image)

    #output_writer = open(args['output'],"w")
    #output_writer.write(text)

    #ocrOnDirectory(args['input'],args['output'])
    #get_tesseract_version()
    print('cleaning and converting')
    #tsv_ocrOnDirectory(args['input'],args['output'])
    tsv_ocrOnDirectory('/project/arcc-students/OilWellProject2023.Summer/Master/non_blank','/project/arcc-students/OilWellProject2023.Summer/generalOCR_MasterNonBlanks')

    return



    

if __name__ =='__main__':
    main()
    