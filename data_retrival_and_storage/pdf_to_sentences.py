import re
import pdf2image
import pytesseract
from pytesseract import Output, TesseractError

pdf_path = '/Users/joshuaodugbemi/Downloads/COMPUTER.pdf'

images = pdf2image.convert_from_path(pdf_path)

def is_page_number(text):
    # Simple heuristic to detect page numbers: a standalone numeric string
    return text.strip().isdigit()

def reconstruct_text(ocr_dict):
    lines = []
    for i in range(len(ocr_dict['text'])):
        if ocr_dict['text'][i].strip():  # If the text element is not empty
            left, top, width, height = [ocr_dict[attr][i] for attr in ['left', 'top', 'width', 'height']]
            lines.append(((top, left), ocr_dict['text'][i]))
    lines.sort(key=lambda x: (x[0][0], x[0][1]))

    reconstructed_text = ""
    for line in lines:
        text = line[1]
        # Remove page numbers
        if not is_page_number(text):
            # Add a newline after a full stop if it's the end of a sentence
            if text.endswith('.'):
                text += "\n"
            reconstructed_text += text + " "
    return reconstructed_text

with open('data_retrival_and_storage/second handbook_final3.txt', 'w') as f:
    for i, pil_im in enumerate(images):
        try:
            ocr_dict = pytesseract.image_to_data(pil_im, config='--oem 1 --psm 3',  lang='eng', output_type=Output.DICT)
            text = reconstruct_text(ocr_dict)
            if text:
                f.write(text + "\n\n")  # Double newline to separate pages
        except TesseractError as e:
            print(f"Error processing page {i+1}: {e}")