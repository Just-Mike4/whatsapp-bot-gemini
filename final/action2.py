import PyPDF2
import nltk

# Open the PDF file
pdf_file = open('data/data.pdf', 'rb')

# Create a PDF reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Extract text from each page of the PDF
text = ''
for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    text += page.extract_text()

# Close the PDF file
pdf_file.close()

# Tokenize the text into sentences
sentences = nltk.sent_tokenize(text)

# Print out the sentences
for i,sentence in enumerate(sentences):
    print(f"number {i}: {sentence}")
    