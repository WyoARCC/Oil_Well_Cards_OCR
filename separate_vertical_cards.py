"""Takes an input directory and moves all of the PDFs in that directory that
have a vertical first page and moves it to the output directory

Written by Cody Sloan
"""
import argparse
import os
import shutil
from PIL import Image
from pdf2image import convert_from_path


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


def convert_pdfs_to_img_dict(filenames, path_to_poppler):
    """Takes a list of PDF file paths, and converts the first page of 
    each PDF to an image, and adds that image to a dictionary with the
    pdf's filename as the key.
    
    Parameters:
        filenames - List of PDF file paths as strings.
        path_to_poppler - String containing the location of your poppler
            installation. This is usually the /bin/ directory in your 
            conda environment.
    Returns:
        img_dict - Dictionary of filename/image pairs of the first page of each
            PDF.
    """
    img_dict = {}
    # Loop over all pdfs and convert the first page to an image
    for filename in filenames:
        # converts only the pdf files and adds them to the list
        img = convert_from_path(filename, \
                                first_page=1, \
                                last_page=1, \
                                poppler_path=path_to_poppler
                               )
        # Add that image to the dictionary with the pdf filename as its key
        img_dict[filename] = img[0]
        
    return img_dict


def move_vertical_cards(filenames, path_to_poppler, save_dir, batch_size=1000):
    """Takes a list of PDF file paths and finds whether or not the first page
    of each PDF is taller than it is wide. If it is, then that path is added
    to a list, which is returned. The PDFs are loaded in batchs of size
    <batch_size> to use memory more efficiently.
    
    Parameters:
        filenames - List of paths to PDF files.
        path_to_poppler - String containing the location of your poppler
            installation. This is usually the /bin/ directory in your 
            conda environment.
        save_dir - String containing path of directory that the PDF files will
            be moved to.
        batch_size - The number of images that will be loaded into memory each
            time convert_pdfs_to_img_dict is ran.
    Returns:
        count - Number of files that were moved.
    """
    count = 0
    # Loop over the filenames list in <batch_size> chunks
    for i in range(0, len(filenames), batch_size):
        # Grab the batch
        batch = filenames[i:i+batch_size]
        # Convert the batch into a filename/image directory
        image_dict = convert_pdfs_to_img_dict(batch, path_to_poppler)
        # Loop over the keys and values of the dictionary
        for path, img in image_dict.items():
            # Grab the image's size and test if it is taller than it is wide
            w, h = img.size
            if h > w:
                count = count + 1
                # If so, add it to the list
                full = os.path.join(save_dir, os.path.basename(path))
                shutil.move(path, full)
    return count


def main():
    # Define poppler path so we can use convert_from_path()
    path_to_poppler = r'/project/arcc-students/csloan5/environments/GPU_env/bin/'
    # Parse input and output directory and batch size arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True,
                        help="Path to directory containing PDF files")
    parser.add_argument("-o", "--output", required=True,
                        help="Path to directory that will be outputted to")
    parser.add_argument("--bs", type=int, default=1000,
                        help="Batch size for converting pdfs to images")
    args = vars(parser.parse_args())
    # Load PDF file names
    filenames = load_pdf_filenames(args["input"])
    # Extract the PDFs that have vertical cards and move them to the new dir
    n_moved_files = move_vertical_cards(filenames, path_to_poppler, args["output"], args["bs"])
    print("Done.", n_moved_files, "files were moved to", args["output"])
    return


if __name__ =='__main__':
    main()
