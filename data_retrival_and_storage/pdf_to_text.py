import cv2
import re
import pdf2image
import pytesseract
from pytesseract import Output, TesseractError
import numpy as np

pdf_path = 'Handbook.pdf'

images = pdf2image.convert_from_path(pdf_path)

def preprocess_image(image):
    # Convert PIL image to OpenCV format
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply adaptive thresholding to binarize the image
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # Denoise (optional, can be commented out if results are not satisfactory)
    # denoised = cv2.fastNlMeansDenoising(thresh, None, 30, 7, 21)
    return thresh

def is_page_number(text):
    # Simple heuristic to detect page numbers: a standalone numeric string
    return text.strip().isdigit()

def clean_text(text, page_number):
    # Remove sequences of dots longer than three
    text = re.sub(r'\.{4,}', '.', text)
    # Remove "LASU STUDENTS’ HANDBOOK" from all pages except the first
    if page_number > 0:
        text = text.replace("LASU STUDENTS’ HANDBOOK", "")
    return text

def reconstruct_text(ocr_dict, page_number):
    lines = []
    for i in range(len(ocr_dict['text'])):
        if ocr_dict['text'][i].strip():  # If the text element is not empty
            left, top, width, height = [ocr_dict[attr][i] for attr in ['left', 'top', 'width', 'height']]
            lines.append(((top, left), ocr_dict['text'][i]))
    lines.sort(key=lambda x: (x[0][0], x[0][1]))

    reconstructed_text = ""
    for line in lines:
        text = line[1]
        # Clean the text
        text = clean_text(text, page_number)
        # Remove page numbers
        if not is_page_number(text):
            # Add a newline after a full stop if it's the end of a sentence
            if text.endswith('.'):
                text += "\n"
            reconstructed_text += text + " "
    return reconstructed_text

with open('data_retrival_and_storage/handbook.txt', 'w') as f:
    for i, pil_im in enumerate(images):
        try:
            preprocessed_image = preprocess_image(pil_im)
            ocr_dict = pytesseract.image_to_data(preprocessed_image, config='--oem 1 --psm 3',  lang='eng', output_type=Output.DICT)
            text = reconstruct_text(ocr_dict, i)  # Pass the page number to the function
            if text:
                f.write(text + "\n\n")  # Double newline to separate pages
        except TesseractError as e:
            print(f"Error processing page {i+1}: {e}")