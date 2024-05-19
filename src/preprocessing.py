import re
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt')

# Read data from file
def read_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Preprocess text
def preprocess_text(text):
    # Remove special characters and convert to lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    return text

# Segment text into sentences
def segment_text(text):
    sentences = sent_tokenize(text)
    return sentences

# Data preprocessing
def process_data(file_path):
    text = read_data(file_path)
    preprocessed_text = preprocess_text(text)
    segments = segment_text(preprocessed_text)
    return segments
