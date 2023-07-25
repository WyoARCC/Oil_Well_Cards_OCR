
import argparse
import layoutDetection.lineDetection as lines
import os
import shutil


#Boolean function to determine if a single path is for a type one card or not
def typeOneTrue(pathToPdf):
    image=lines.firstPageToImage(pathToPdf)
    dim=image.shape
    #if the card is of veticle orientation we throw it out
    if dim[0]>dim[1]:
        return False
    #I am not sure why, but this setup with two line sets seems to work better than just -.78 to .78
    vlines=lines.findLines(image,0,.78)
    vlines2=lines.findLines(image,-.78,.78)
        
    if vlines is None and vlines2 is None:       
        return False
    else:    
        return True
    return False

#this function is hardcoded to our original path and filters all of the cards
#TODO
"""
def filterAllOilCards(destination):
    for folder in  os.listdir('/project/arcc-students/enhanced_oil_recovery_cards'):
        os.makedirs(os.path.join(destination,folder), exist_ok=True)
        for folder2 in os.listdir(os.path.join('/project/arcc-students/enhanced_oil_recovery_cards',folder)):            
            ocrOnDirectory(os.path.join('/project/arcc-students/enhanced_oil_recovery_cards',folder,folder2),os.path.join(destination,folder))
"""
def filterDirectoryRecursive(directory,output):
    filenames=load_pdf_filenames(directory)
    print('These files were filtered OUT')
    for file in filenames:
        if typeOneTrue(file):
            shutil.copy(file, os.path.join(output,str(file.split('/')[-1])))
        else:
            print(str(file))

def load_pdf_filenames(pdf_dir):
    """Takes a path to a directory with PDFs, then adds all of the paths of
    the PDF files in that directory to the filenames list, which is returned.
    
    Parameters:
        pdf_dir - String containing file system location of PDF files.
    Returns:
        filenames - Updated list of PDF file paths.
    """
    filenames = []
    # Scan recursively over all pdf files in a directory
    for folder, subfolders, files in os.walk(pdf_dir):
        for file in files:
            if file.endswith('.pdf'):
                #Add all the .pdf filenames to a list
                filename = os.path.join(folder, file)
                filenames.append(filename)
                
    return filenames
    

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True,
    	help="path to input pdf file")     
    ap.add_argument("-o", "--output", required=False,
        help="path to output file") 
    ap.add_argument("-f", "--filtered", required=False,
        help="path to text file listeing files that were filtered out") 
    args = vars(ap.parse_args())
    #typeOneTrue(args['input'])
    filterDirectoryRecursive(args['input'],args['output'])
    print('done')

    return

if __name__ =='__main__':

    main()