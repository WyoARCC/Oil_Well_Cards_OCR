#Attempting to detect where the layout defining lines are in a oil card
#To be used on type of card seen in 310-0000 which has 4 distinct sections
#https://hackthedeveloper.com/line-detection-opencv-python/
#by Collin Dixon
import cv2
from pdf2image import convert_from_path
import os
import sys
import numpy
import argparse



#takes an image and outputs the detected lines
#the theta variables specify the angle of lines to be detected and are set to detect all lines by default
#I use .78 and 2.35 to fine horizontal lines
#-.78 and.78 for verticle
def findLines(image,min_theta = 0,max_theta = numpy.pi,threshold = 242):
    grayscaled = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(grayscaled,165,255,cv2.THRESH_BINARY)[1]
    kernel = numpy.ones((15,1), numpy.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    kernel = numpy.ones((17,3), numpy.uint8)
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)
    edges = cv2.Canny(grayscaled, 50, 150, apertureSize=3)
    #lines = cv2.HoughLinesP(edges, rho=1, theta=numpy.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
    lines = cv2.HoughLines(edges, rho=1, theta=numpy.pi/180, threshold=242, min_theta=min_theta, max_theta= max_theta)
    
    return lines



#assumes jpeg. draws lines on an image and outputs result
def drawLines(image,lines):
    for line in lines:
        rho, theta = line[0]
        a = numpy.cos(theta)
        b = numpy.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return image

#recursivly finds lines when given an input directory. outputs to output path given
def findAndDrawLinesRecursive(input,output):
    for file in os.listdir(input):
        filePath=os.path.join(input,file)
        if os.path.isdir(filePath):
            newInput=os.path.join(input,file)
            newOutput=os.path.join(output,file)
            os.makedirs(newOutput, exist_ok=True)
            findAndDrawLinesRecursive(newInput,newOutput)
        if os.path.isfile(filePath):
            image=firstPageToImage(filePath)
            lines=findLines(image)
            image=drawLines(image,lines)
            cv2.imwrite(os.path.join(output,str(file)+".jpg"),image)
            print(os.path.join(output,str(file)+".jpg"))

#converts the first page of a pdf to cv2-able image
def firstPageToImage(pdfPath):
    pages = convert_from_path(pdfPath)
    img = numpy.array(pages[0])
    return img

#this a redundant implementation for now. But I think I may find better ways to get the best line in the future
#intended for use on horizontal lines
def getBestLine(lines):
    print(lines[0][0])
    return lines[0][0]

#intended for use on vertical lines
#will sort lines from left to right
#write a readable function, difficulty level: impossible
#outputs an array of lists, each list containing a tuple representing a line. The output is set this way in order to match the built in cv2 houghlines function
def getBestTwoLines(lines):
    #setting a default in case less than 2 lines were detected
    #this array is triple nested so that it matches the way cv2.houghlines() outputs its list of lines
    bestTwo=[[[0,0]],[[0,0]]]
    i=0
    for line in lines:
        #first check if it is too close to any other stored line
        less=False
        for line2 in bestTwo:
            #print(abs(float(line[0][0])-float(line2[0][0])))
            if abs(float(line[0][0])-float(line2[0][0]))<100:
                less=True
                break
        #if it is not too close, add to bestThree
        if not less:
            bestTwo[i]=line
            i+=1
        if i>1:
            break
    #sort by horizontal coord
    bestTwo.sort(key=lambda x: x[0][0])
    #print(bestTwo)
    return bestTwo

#takes a cv2 image and splits it into four parts based on the lines given
def splitImage(image,horizontal,vertical):
    dim=image.shape
    print(vertical)
    topImage=image[0:int(horizontal[0]),0:dim[1]]
    bottomImage=image[int(horizontal[0]):dim[0],0:dim[1]]
    dim2=bottomImage.shape
    print(dim2[0])
    print(vertical[0][0][0])
    leftImage=bottomImage[0:dim2[0],0:int(vertical[0][0][0])]
    centerImage=bottomImage[0:dim2[0],int(vertical[0][0][0]):int(vertical[1][0][0])]
    rightImage=bottomImage[0:dim2[0],int(vertical[1][0][0]):dim2[1]]
    
    return topImage,leftImage,centerImage,rightImage


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True,
    	help="path to input pdf file") 
    
    ap.add_argument("-o", "--output", required=True,
        help="path to output file") 
    args = vars(ap.parse_args())
    #findAndDrawLinesRecursive(args['input'],args['output'])
    image=firstPageToImage(args['input'])
    #finding vertical lines
    linesV=findLines(image,-.78,.78)
    image=drawLines(image,linesV)
    cv2.imwrite(args['output'], image)
    """
    linesV=findLines(image,-.78,.78)
    linesV=getBestTwoLines(linesV)
    linesH=findLines(image,.78, 2.35)
    linesH=getBestLine(linesH)
    #image1=drawLines(image,lines)
    topImage,leftImage,centerImage,rightImage=splitImage(image,linesH,linesV)
    cv2.imwrite(os.path.join(args['output'],"topImage.jpg"), topImage)
    cv2.imwrite(os.path.join(args['output'],"leftImage.jpg"), leftImage)
    cv2.imwrite(os.path.join(args['output'],"centerImage.jpg"), centerImage)
    cv2.imwrite(os.path.join(args['output'],"rightImage.jpg"), rightImage)
    """
    return

if __name__ =='__main__':

    main()
    