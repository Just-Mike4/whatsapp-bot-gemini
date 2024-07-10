import google.generativeai as genai
import os
import spacy
import pandas as pd
import string
import numpy as np
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import language_tool_python


tool = language_tool_python.LanguageToolPublicAPI('en-US')

load_dotenv()


# Initialize SpaCy, punctuation, stopwords, and LanguageTool
nlp = spacy.load('en_core_web_sm')
punc = string.punctuation
stopwords = list(spacy.lang.en.stop_words.STOP_WORDS)

# Load the preprocessed data
df = pd.read_csv('/Users/joshuaodugbemi/Desktop/Major Projects/Final Year Project/data_retrival_and_storage/handbook2.csv')

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

# Define a function to generate a summary based on the user input
def generate_summary(user_input):
    cleaned_input = ' '.join(text_cleaner(user_input))
    input_vector = vectorizer.transform([cleaned_input])
    similarities = cosine_similarity(input_vector, vectorizer.transform(df['Sentence']))
    best_match_index = np.argmax(similarities)
    summary = df.loc[best_match_index, 'Sentence']
    score = similarities[0, best_match_index]
    return summary, score

def generate_response(prompt):
  GOOGLE_API_KEY= os.getenv('GOOGLE_API_KEY')
  genai.configure(api_key=GOOGLE_API_KEY)
  model = genai.GenerativeModel('gemini-1.5-flash')
  response = model.generate_content(prompt)
  return response.text

def correct_grammar(text):
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text

# Define a function to handle user input and generate a response
def handle_user_input(user_input):
    summary, score = generate_summary(user_input)
    corrected_summary = correct_grammar(summary)  # Correct grammatical errors in the summary
    response = generate_response(user_input)
    return corrected_summary, score, response


def main():
  print("Hi! I'm your conversational AI Assistant and Text summarization bot, How can i help you today?")
  while True:
    user_input = input("Ask a question (or type 'exit' to quit): ")
    if user_input.lower() == "exit":
      break
    summary, score, response = handle_user_input(user_input)
    if score>0:
        print(f"Chatbot: {summary}")
    else:
        print(f"Chatbot: {response}")

if __name__ == "__main__":
  main()