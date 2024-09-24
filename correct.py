import google.generativeai as genai
import os

# Set your Google API key
GOOGLE_API_KEY = 'AIzaSyC3f8pktqTkV6Y_AJsxELRzmZfPYAtES1M'

# Initialize Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def correct_text(text):
    response = model.generate_content(f"Correct grammar, punctuation, and spelling errors Dont say anything afterwards just the corrected text and remove words or text or character that cant be understood put listed things together and arrange well: {text}")
    return response.text

# Input and output file paths
input_file = '/Users/joshuaodugbemi/Desktop/Major Projects/Final Year Project/ocr_handbook.txt'
output_file = 'corrected_final.txt'

# Read input file, correct text, and write to output file
with open(input_file, 'r') as input_f, open(output_file, 'a') as output_f:
    lines = input_f.readlines()[8000:]  # Read first 500 lines
    text_to_correct = ''.join(lines)  # Concatenate lines into a single string
    corrected_text = correct_text(text_to_correct)  # Correct the text as a whole
    output_f.write(corrected_text + '\n')  # Write the corrected text to the output file

print("Text correction complete.")