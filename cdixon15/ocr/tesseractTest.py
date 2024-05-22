import numpy as np
import pytesseract
import argparse
import cv2
import os
import sys

from pdf2image import convert_from_path


def main():
    #do all the main stuff

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True,
    	help="path to input directory") 
    ap.add_argument("-o", "--output", required=True,
        help="path to directory of text files") 
    args = vars(ap.parse_args())
    
    #text=ocr_core(convert_from_path(os.path.join(directory,str(file)))[0], 3)
    image=convert_from_path(args['input'])

    text=pytesseract.image_to_string(image[0])
    output_writer = open(os.path.join(args['output'],'string'), "w")
    output_writer.write(text)

    text=pytesseract.image_to_boxes(image[0])
    output_writer = open(os.path.join(args['output'],'boxes'), "w")
    output_writer.write(text)

    text=pytesseract.image_to_data(image[0])
    output_writer = open(os.path.join(args['output'],'data'), "w")
    output_writer.write(text)

    text=pytesseract.image_to_osd(image[0])
    output_writer = open(os.path.join(args['output'],'osd'), "w")
    output_writer.write(text)

    text=pytesseract.image_to_alto_xml(image[0])
    output_writer = open(os.path.join(args['output'],'xml'), "w")
    output_writer.write(text)


    return



    

if __name__ =='__main__':
    main()
    