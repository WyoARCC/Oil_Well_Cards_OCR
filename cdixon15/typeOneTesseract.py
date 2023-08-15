import layoutDetection.lineDetection
import ocr.cleanAndConvert

import os


def typeOneOCR(image):   
    
    linesV=layoutDetection.lineDetection.findLines(image,-.78,.78)
    linesV=layoutDetection.lineDetection.getBestTwoLines(linesV)
    linesH=layoutDetection.lineDetection.findLines(image,.78, 2.35)
    linesH=layoutDetection.lineDetection.getBestLine(linesH)    

    topImage,leftImage,centerImage,rightImage=layoutDetection.lineDetection.splitImage(image,linesH,linesV)

    textTop=ocr.cleanAndConvert.ocr_core(topImage, 3)
    textLeft=ocr.cleanAndConvert.ocr_core(leftImage, 3)
    textCenter=ocr.cleanAndConvert.ocr_core(centerImage, 3)
    textRight=ocr.cleanAndConvert.ocr_core(rightImage, 3)

    #the section labels may need to be replaced to make sure they are unique from raw OCR output and easy to parse
    textFull="--SECTIONLABELTOP: "+os.linesep+textTop+os.linesep+ \
            "--SECTIONLABELLEFT: "+os.linesep+textLeft+os.linesep+ \
            "--SECTIONLABELCENTER: "+os.linesep+textCenter+os.linesep+ \
            "--SECTIONLABELRIGHT: "+os.linesep+textRight

    
    return textFull

def main():

    return

if __name__ =='__main__':
    main()