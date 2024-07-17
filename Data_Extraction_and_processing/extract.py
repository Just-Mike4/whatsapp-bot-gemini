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
current_section = {"header": "", "paragraphs": []}

for page_num in range(len(pdf_reader.pages)):
	page = pdf_reader.pages[page_num]
	page_text = page.extract_text()
	page_text = remove_page_numbers(page_text)
	lines = page_text.splitlines()

	i = 0
	while i < len(lines):
		line = lines[i]
		# Peek ahead to see if the next line is also a header or a continuation of a header
		if i + 1 < len(lines) and (is_header(line) and is_header(lines[i + 1])):
			# Combine current and next line as they are both headers or continuation of a header
			line += " " + lines[i + 1]
			i += 1  # Skip the next line as it's already included

		if is_header(line):
			if current_section["header"] or current_section["paragraphs"]:
				sections.append(current_section)
				current_section = {"header": "", "paragraphs": []}
			current_section["header"] = line
		elif is_not_empty(line):
			current_section["paragraphs"].append(line)
		i += 1

if current_section["header"] or current_section["paragraphs"]:
	sections.append(current_section)

pdf_file.close()

json_output = json.dumps(sections, indent=4)

with open('Data_Extraction_and_processing/extracted_text.json', 'w') as json_file:
	json_file.write(json_output)
