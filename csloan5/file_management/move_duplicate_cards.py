"""This script first finds all of the filenames of the pdf files in a
directory, and then searches another directory to check if those files can be
found in there. If there are matching files, they get moved to another
directory specified by the user.

Written by Cody Sloan
"""
import os
import shutil
import argparse

def load_filenames(directory):
    filenames = []
    # Scan recursively over all pdf files in a directory
    for folder, subfolders, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                #Add all the .pdf filenames to a list
                filenames.append(file)
                
    return filenames


def move_files(original_files, dupe_file_dir, destination):
    count = 0
    for file in original_files:
        filename = os.path.join(dupe_file_dir, file)
        if os.path.exists(filename):
            shutil.move(filename, destination)
            count += 1
    return count


def main():
    # Parse input and output directory and batch size arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=str,
                        help="Path to directory containing original files")
    parser.add_argument("--dupe", required=True, type=str,
                        help="Path to directory that has duplicated files")
    parser.add_argument("-o", "--output", required=True, type=str,
                        help="Directory path that files will get moved to")
    args = vars(parser.parse_args())
    filenames = load_filenames(args["source"])
    
    num_files = move_files(filenames, args["dupe"], args["output"])
    print("Done,", num_files, "files were moved from", args["dupe"], "to", 
          args["output"])
    return
    
    
if __name__ == "__main__":
    main()