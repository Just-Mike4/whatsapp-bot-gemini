import spacy
import pandas as pd
import string
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import language_tool_python
import numpy as np
from chatterbot.trainers import ChatterBotCorpusTrainer
from summarizingmodel import generate_summarized_text

class ENGSM:
    ISO_639_1 = 'en_core_web_sm'

# Initialize SpaCy, punctuation, stopwords, and LanguageTool
nlp = spacy.load('en_core_web_sm')
punc = string.punctuation
stopwords = list(spacy.lang.en.stop_words.STOP_WORDS)
tool = language_tool_python.LanguageTool('en-US')

# Load the preprocessed data
df = pd.read_csv('data/data2.csv')

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

# Create a TfidfVectorizer object
vectorizer = TfidfVectorizer(stop_words='english')
vectorizer.fit(df['Sentence'])

# Initialize ChatterBot
chatbot = ChatBot('New Bot', tagger_language=ENGSM)


# Define a function to generate a summary based on the user input
def generate_summary(user_input):
    cleaned_input = ' '.join(text_cleaner(user_input))
    input_vector = vectorizer.transform([cleaned_input])
    similarities = cosine_similarity(input_vector, vectorizer.transform(df['Sentence']))
    best_match_index = np.argmax(similarities)
    summary = df.loc[best_match_index, 'Sentence']
    score = similarities[0, best_match_index]
    return summary, score

# Define a function to handle user input and generate a response
def handle_user_input(user_input):
    summary, score = generate_summary(user_input)
    response = chatbot.get_response(user_input)
    return summary, score, response

# Interactive loop for testing
user_input = input("Ask a question (or type 'exit' to quit): ")
while user_input.lower() != 'exit':
    summary, score, response = handle_user_input(user_input)
    if score>0:
        # summary= generate_summarized_text(summary, 2)
        print(f"Chatbot: {summary}")
    else:
        print(f"Chatbot: {response}")
    user_input = input("Ask a question (or type 'exit' to quit): ")
