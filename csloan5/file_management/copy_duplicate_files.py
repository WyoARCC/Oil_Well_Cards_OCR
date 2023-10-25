"""This script first finds all of the filenames of the pdf files in a
directory, and then searches another directory to check if those files can be
found in there. If there are matching files, they get moved to another
directory specified by the user.

Written by Cody Sloan
"""
import os
import shutil
import argparse

def load_filenames(directory, remove_file_ext=False, add_parent_folder=False, use_entire_path=False):
    filenames = []
    if add_parent_folder and use_entire_path:
        print("'add_parent_folder' and 'use_entire_path' options are mutually exclusive!", file=sys.stderr)
        quit()
    # Scan recursively over all pdf files in a directory
    for folder, subfolders, files in os.walk(directory):
        for file in files:
            f = file
            if remove_file_ext:
                f = os.path.splitext(f)[0]

            if use_entire_path:
                f = os.path.join(folder, f)
                
            if add_parent_folder:
                subfolder = os.path.basename(folder)
                f = os.path.join(subfolder, f)
            
            filenames.append(f)    
    return filenames


def copy_files(copy_filenames, copy_dir, source_dir, output_dir):
    count = 0
    for file in copy_filenames:
        filename = os.path.join(source_dir, os.path.basename(file))
        if os.path.exists(filename):
            output_subdir = os.path.join(output_dir, os.path.dirname(file))
            os.makedirs(output_subdir, exist_ok=True)
            
            copy_filename = os.path.join(copy_dir, file + '.csv')
            
            shutil.copy(copy_filename, output_subdir)
            count += 1
    return count

def main():
    # Parse input and output directory and batch size arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--copy", required=True, type=str,
                        help="Path to directory containing files that will be copied")
    parser.add_argument("--source", required=True, type=str,
                        help="Path to directory that the copy directory will be compared to")
    parser.add_argument("-o", "--output", required=True, type=str,
                        help="Directory path that files will get copied to")
    args = vars(parser.parse_args())
    
    copy_filenames = load_filenames(args["copy"], remove_file_ext=True, add_parent_folder=True)
    
    num_files = copy_files(copy_filenames, args["copy"], args["source"], args["output"])
    print("Done,", num_files, "files were moved from", args["copy"], "to", 
          args["output"])
    return
    
    
if __name__ == "__main__":
    main()