import PyPDF2
import re

# Function to remove page numbers
def remove_page_numbers(text):
    patterns = [
        r'Page \d+',  # Matches "Page" followed by a space and a number
        r'^\d+\s|\s\d+\s|\s\d+$',  # Matches standalone numbers at the start, middle, or end of the text
    ]
    for pattern in patterns:
        text = re.sub(pattern, '', text)
    return text

# Open the PDF file
pdf_file = open('/Users/joshuaodugbemi/Downloads/COMPUTER.pdf', 'rb')

# Create a PDF reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Extract text from each page of the PDF and remove page numbers
text = ''
for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    page_text = page.extract_text()
    page_text = remove_page_numbers(page_text)
    text += page_text

# Close the PDF file
pdf_file.close()

# Write the cleaned text to a new file
with open('data/data3.txt', 'w') as f:
    f.write(text)