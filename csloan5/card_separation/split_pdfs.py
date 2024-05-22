import os
from PyPDF2 import PdfReader, PdfWriter
import argparse

def is_blank_page(page, black_threshold=0.4):
    content = page.extract_text().strip()
    if len(content) > 0:
        return False
    
    # Get the page's dimensions using rectangle coordinates
    x0, y0, x1, y1 = page.mediabox.lower_left + page.mediabox.upper_right
    width = x1 - x0
    height = y1 - y0

    # Check if the page has image content
    if '/XObject' not in page['/Resources']:
        return True

    # Get the page's pixel data as a byte string
    xobjects = page['/Resources']['/XObject']
    image_objects = [xobjects[obj] for obj in xobjects if xobjects[obj]['/Subtype'] == '/Image']
    if not image_objects:
        return True

    # Calculate the percentage of black pixels relative to the total number of pixels
    total_pixels = width * height
    black_pixels = 0

    for image_object in image_objects:
        image_data = image_object.get_data()
        black_pixels += sum(1 for pixel in image_data if pixel < 128)

    black_percentage = black_pixels / total_pixels

    return black_percentage <= black_threshold


def split_pdf_by_blank_pages(input_folder, blank_output_folder, non_blank_output_folder, batch_size=1000, black_threshold=0.4):
    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith('.pdf'):
                input_pdf_path = os.path.join(root, filename)

                with open(input_pdf_path, 'rb') as file:
                    reader = PdfReader(file)
                    total_pages = len(reader.pages)

                    for start_page in range(0, total_pages, batch_size):
                        end_page = min(start_page + batch_size, total_pages)
                        output_pages = []

                        for page_number in range(start_page, end_page):
                            page = reader.pages[page_number]
                            is_blank = is_blank_page(page, black_threshold)

                            if is_blank:
                                output_folder = blank_output_folder
                                output_pages.append((page, output_folder, filename, page_number + 1))
                            else:
                                output_folder = non_blank_output_folder
                                output_pages.append((page, output_folder, filename, page_number + 1))
                            

                        # Process the batch of pages
                        for page, output_folder, filename, page_number in output_pages:
                            output_path = os.path.join(output_folder, f'{filename}_page_{page_number}.pdf')

                            writer = PdfWriter()
                            writer.add_page(page)

                            with open(output_path, 'wb') as output_file:
                                writer.write(output_file)

    print("PDF processing completed.")
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True,
                        help="Path to directory containing PDF files")
    parser.add_argument("--not", required=True,
                        help="Path to directory that non-blank pages will be outputted to")
    parser.add_argument("--blank", required=True,
                        help="Path to directory that blank pages will be outputted to")
    args = vars(parser.parse_args())

    # Create the output folders if they don't exist
    os.makedirs(args["blank"], exist_ok=True)
    os.makedirs(args["not"], exist_ok=True)

    split_pdf_by_blank_pages(args["input"], args["blank"], args["not"], batch_size=1000, black_threshold=0.4)
    return

if __name__ =='__main__':
    main()