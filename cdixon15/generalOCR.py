
import argparse
import ocr.cleanAndConvert 

from turtle import left, right
import numpy as np
import pytesseract
import imutils
import cv2
from pdf2image import convert_from_path
import os
import sys

import psutil
from multiprocessing import Pool



#run from cleanandconvert for now
def main():
    print('hello')
    output_writer = open('/project/arcc-students/cdixon15/oilCardProject/oil_Card_Git/Oil_Well_Cards_OCR/cdixon15/processed/generalOCR/out.txt', "w")
    output_writer.write('start')
    
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True,
    	help="path to input directory") 
    ap.add_argument("-o", "--output", required=True,
        help="path to directory of text files") 
    args = vars(ap.parse_args())
   
    pool=Pool(psutil.cpu_count(logical=False))

    ocr.cleanAndConvert.tsv_ocrOnDirectory(args['input'],args['output'])
    
    return

if __name__ =='__main__':
    main()