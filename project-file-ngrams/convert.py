import cv2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    # Convert PIL Image to NumPy array for OpenCV processing
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding (binarization)
    _, binary_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    
    # Apply Gaussian blur to reduce noise
    blurred_img = cv2.GaussianBlur(binary_img, (1, 1), 0)

    # Convert back to PIL Image format
    return Image.fromarray(blurred_img)

def pdf_to_text(pdf_path, output_txt_path):
    images = convert_from_path(pdf_path,poppler_path=r'C:\Users\user\poppler-24.07.0\Library\bin')
    full_text = ""

    for i, image in enumerate(images):
        # Preprocess the image
        preprocessed_image = preprocess_image(image)
        
        # Extract text from the preprocessed image
        text = pytesseract.image_to_string(preprocessed_image)
        
        full_text += text + "\n\n"
        print(f"Processed page {i + 1}/{len(images)}")

    with open(output_txt_path, 'w', encoding='utf-8') as file:
        file.write(full_text)
    
    print(f"Text extracted and saved to {output_txt_path}")

# Example usage
pdf_path = r'C:\Users\user\Desktop\Final Project\final-year-proj\Docs\General-handbook.pdf'  
output_txt_path = 'ocr_handbook.txt'  

pdf_to_text(pdf_path, output_txt_path)
