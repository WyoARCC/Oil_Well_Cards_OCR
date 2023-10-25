from PIL import Image
import os
from pdf2image import convert_from_path

def convert_pdfs(pdf_dir, path_to_poppler):
    output = r'/project/arcc-students/csloan5/OilWellCards_project/all_first_pages/'

    for folder, subfolders, files in os.walk(pdf_dir):
        for file in files:
            path = os.path.join(folder, file)
            img = convert_from_path(path,
                                    first_page=1,
                                    last_page=1,
                                    poppler_path=path_to_poppler
                                   )
            img[0].save(output + file[:8] +'.jpg')
        
def main():
    pdf_dir = r'/project/arcc-students/enhanced_oil_recovery_cards/'
    path_to_poppler = r'/project/arcc-students/csloan5/environments/GPU_env/bin/'
    convert_pdfs(pdf_dir, path_to_poppler)
    return
    
if __name__ =='__main__':
    main()