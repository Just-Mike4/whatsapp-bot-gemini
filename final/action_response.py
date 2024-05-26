import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
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
df = pd.read_csv('data/data.csv')

# Create a TfidfVectorizer object
vectorizer = TfidfVectorizer(stop_words='english')

# Fit the vectorizer to the combined cleaned text column
vectorizer.fit(df['Corrected Text'])

# Create a continuous Q&A bot
while True:
    # Ask the user for a question
    question = input("Ask a question (or type 'exit' to quit): ")

    # If the user types 'exit', break out of the loop
    if question.lower() == 'exit':
        break

    # Clean the question using the text_cleaner function
    cleaned_question = ' '.join(text_cleaner(question))

    # Vectorize the cleaned question
    question_vector = vectorizer.transform([cleaned_question])

    # Calculate the cosine similarity between the question and the combined cleaned text
    similarities = cosine_similarity(question_vector, vectorizer.transform(df['Corrected Text']))

    # Get the index of the row with the highest similarity score
    best_match_index = np.argmax(similarities)

    # Get the corrected text from the row with the highest similarity score
    summary = df.loc[best_match_index, 'Corrected Text']

    # Print the summary
    print(summary)