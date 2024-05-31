import re
import numpy as np
import pandas as pd
import string
from spacy.lang.en.stop_words import STOP_WORDS
import spacy
import language_tool_python

# Initialize punctuation and stopwords
punc = string.punctuation
stopwords = list(STOP_WORDS)
nlp = spacy.load('en_core_web_sm')
tool = language_tool_python.LanguageTool('en-US')

def text_cleaner(sentence):
    # Ensure the sentence is a string
    if sentence is None:
        sentence = ""
    doc = nlp(sentence)
    
    tokens = []
    for token in doc:
        if token.lemma_ != "-PRON-":
            temp = token.lemma_.lower().strip()
        else:
            temp = token.lower_
        tokens.append(temp)
        
    cleaned_tokens = []
    for token in tokens:
        if token not in stopwords and token not in punc:
            cleaned_tokens.append(token)
    return cleaned_tokens

# Load the preprocessed data
with open('data/data.txt', 'r') as file:
    text = file.read()

# Preprocess text
headings = []
sentences = []
current_heading = None
sentence = ''
for line in text.splitlines():
    if line.isupper(): 
        current_heading = line
        headings.append(line)
    else:
        if line.strip():  # If line is not empty
            sentence += line + ''
        else:  # If line is empty, it marks the end of a sentence
            if sentence:
                sentences.append((current_heading, sentence.strip()))  # Associate sentence with current heading
                sentence = ''
        if line.endswith('.'):  # If line ends with a full stop, it marks the end of a sentence
            sentences.append((current_heading, sentence.strip()))  # Associate sentence with current heading
            sentence = ''

# Create numpy array
data = np.zeros((len(sentences), 6), dtype=object)
for i, (heading, sentence) in enumerate(sentences):
    # Ensure heading and sentence are strings
    
    
    data[i, 0] = heading
    data[i, 1] = sentence
    data[i, 2] = ' '.join(text_cleaner(heading))  
    data[i, 3] = ' '.join(text_cleaner(sentence))
    data[i, 4] = ' '.join(text_cleaner(heading)) + ' ' + ' '.join(text_cleaner(sentence))  # Combined cleaned text
    data[i, 5] = tool.correct(heading + ' ' + sentence)  # Correct grammatical errors

# Print table
df = pd.DataFrame(data, columns=['Heading', 'Sentence', 'Cleaned Heading', 'Cleaned Sentence', 'Combined Cleaned Text', 'Corrected Text'])
# print(df.head(20))
# print(df.tail(20))
df.to_csv('data/data2.csv', index=False)