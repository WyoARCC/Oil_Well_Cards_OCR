import io
import os
from google.cloud import vision
from pdf2image import convert_from_path

poppler = "/project/arcc-students/csloan5/environments/GPU_env/bin/"

# Set up Vision client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/project/arcc-students/crothfu1/OilWellProject/Code/savvy-hybrid-389017-984cabbf64b0.json' 
client = vision.ImageAnnotatorClient()

# Folder containing PDFs
pdf_folder = '/project/arcc-students/crothfu1/OilWellProject/Code/BlankPages/VertNonBlank'
output_folder = '/project/arcc-students/crothfu1/OilWellProject/Code/CloudVisionText'
text_check_folder = '/project/arcc-students/crothfu1/OilWellProject/Code/CloudVisionText'

# Loop through all PDFs in folder
for pdf_path in os.listdir(pdf_folder):
    if pdf_path.endswith('.pdf'):
        
        # Get filename without extension
        filename = os.path.splitext(pdf_path)[0]

        # Check text file folder for existing text file
        text_path = os.path.join(text_check_folder, f"{filename}.txt")
        if os.path.exists(text_path):
            print(f"{text_path} exists, skipping OCR")
            continue
            
            
        # Convert PDF to image
        images = convert_from_path(os.path.join(pdf_folder, pdf_path),poppler_path=poppler)
        image = images[0]
        
        # Convert image to bytes (what google cloud vision uses as their input)
        buf = io.BytesIO()
        image.save(buf, format='JPEG')
        byte_im = buf.getvalue()
        
        # Perform OCR
        image = vision.Image(content=byte_im)
        response = client.document_text_detection(image=image, image_context={"language_hints": ['en']})
        
        # Extract text
        extracted_text = response.full_text_annotation.text
        
        # Save text to output folder
        text_path = os.path.splitext(pdf_path)[0] + '.txt'
        output_path = os.path.join(output_folder, text_path)
        with open(output_path, 'w') as text_file:
            text_file.write(extracted_text)
            
print('OCR complete for all PDFs in folder')