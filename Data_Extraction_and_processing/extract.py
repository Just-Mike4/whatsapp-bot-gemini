import PyPDF2
import re
import json

def remove_page_numbers(text):
	patterns = [r'Page \d+', r'^\d+\s|\s\d+\s|\s\d+$']
	for pattern in patterns:
		text = re.sub(pattern, '', text)
	return text

def is_header(line):
	return line.isupper() or potential_header_within_paragraph(line)

def potential_header_within_paragraph(line):
	# Adjust this regex to match your specific header format, including continuations
	return re.match(r'^CSC \d{3}:', line) or re.match(r'^- [A-Z]', line)

def is_not_empty(line):
	# Check if the line is not empty or does not contain only whitespace
	return line.strip() != ''

pdf_file_path = '/Users/joshuaodugbemi/Desktop/Major Projects/Final Year Project/HandbookCS.pdf'
pdf_file = open(pdf_file_path, 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

sections = []

for page_num in range(len(pdf_reader.pages)):
	page = pdf_reader.pages[page_num]
	page_text = page.extract_text()
	page_text = remove_page_numbers(page_text)
	lines = page_text.splitlines()

	i = 0
	paragraph_lines = []  # Temporary variable to accumulate lines for a paragraph
	current_header = ""
	while i < len(lines):
		line = lines[i]
		if i + 1 < len(lines) and (is_header(line) and is_header(lines[i + 1])):
			line += " " + lines[i + 1]
			i += 1

		if is_header(line):
			if current_header or paragraph_lines:
				# Join accumulated lines with a line break and add as a single paragraph
				extracted_portion = current_header + '\n' + '\n'.join(paragraph_lines)
				sections.append({"extracted_portion": extracted_portion})
				paragraph_lines = []  # Reset for the next paragraph
				current_header = ""
			current_header = line
		elif is_not_empty(line):
			paragraph_lines.append(line)
		i += 1

	# Add the last accumulated paragraph if any
	if current_header or paragraph_lines:
		extracted_portion = current_header + '\n' + '\n'.join(paragraph_lines)
		sections.append({"extracted_portion": extracted_portion})

pdf_file.close()

json_output = json.dumps(sections, indent=4)

with open('Data_Extraction_and_processing/extracted_text.json', 'w') as json_file:
	json_file.write(json_output)
