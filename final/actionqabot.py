import spacy
import pandas as pd
import string
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import language_tool_python
import numpy as np

class ENGSM:
    ISO_639_1 = 'en_core_web_sm'

# Initialize SpaCy, punctuation, stopwords, and LanguageTool
nlp = spacy.load('en_core_web_sm')
punc = string.punctuation
stopwords = list(spacy.lang.en.stop_words.STOP_WORDS)
tool = language_tool_python.LanguageTool('en-US')

# Load the preprocessed data
df = pd.read_csv('data/data.csv')

def text_cleaner(sentence):
    if sentence is None:
        sentence = ""
    doc = nlp(sentence)
    tokens = [token.lemma_.lower().strip() if token.lemma_ != "-PRON-" else token.lower_ for token in doc]
    cleaned_tokens = [token for token in tokens if token not in stopwords and token not in punc]
    return cleaned_tokens

# Create a TfidfVectorizer object
vectorizer = TfidfVectorizer(stop_words='english')
vectorizer.fit(df['Corrected Text'])

# Initialize ChatterBot
chatbot = ChatBot('Charlie', tagger_language=ENGSM)
trainer = ListTrainer(chatbot)

# Load and train the chatbot with the dialogue file
with open('final/dialogs.txt', 'r') as file:
    dialogues = file.readlines()

conversation_pairs = []
for dialogue in dialogues:
    if '\t' in dialogue:
        pair = dialogue.strip().split('\t')
        if len(pair) == 2:
            conversation_pairs.append(pair)

for pair in conversation_pairs:
    trainer.train(pair)

# Define a function to generate a summary based on the user input
def generate_summary(user_input):
    cleaned_input = ' '.join(text_cleaner(user_input))
    input_vector = vectorizer.transform([cleaned_input])
    similarities = cosine_similarity(input_vector, vectorizer.transform(df['Corrected Text']))
    best_match_index = np.argmax(similarities)
    summary = df.loc[best_match_index, 'Corrected Text']
    return summary

# Define a function to handle user input and generate a response
def handle_user_input(user_input):
    summary = generate_summary(user_input)
    response = chatbot.get_response(user_input)
    return summary, response

# Interactive loop for testing
user_input = input("Ask a question (or type 'exit' to quit): ")
while user_input.lower() != 'exit':
    summary, response = handle_user_input(user_input)
    print(f"Summary: {summary}")
    print(f"Chatbot: {response}")
    user_input = input("Ask a question (or type 'exit' to quit): ")
