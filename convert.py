import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os


pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'  

def pdf_to_text(pdf_path, output_txt_path):
    
    images = convert_from_path(pdf_path)
    
    
    full_text = ""
    
    
    for i, image in enumerate(images):
        
        text = pytesseract.image_to_string(image)
        
        
        full_text += text + "\n\n"
        
        print(f"Processed page {i + 1}/{len(images)}")
    
    
    with open(output_txt_path, 'w', encoding='utf-8') as file:
        file.write(full_text)
    
    print(f"Text extracted and saved to {output_txt_path}")

# Example usage
pdf_path = 'Handbook.pdf'  
output_txt_path = 'OCRhandbook.txt'  

pdf_to_text(pdf_path, output_txt_path)