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
from rouge_score import rouge_scorer

tool = language_tool_python.LanguageToolPublicAPI('en-US')

load_dotenv()


# Initialize SpaCy, punctuation, stopwords, and LanguageTool
nlp = spacy.load('en_core_web_sm')
punc = string.punctuation
stopwords = list(spacy.lang.en.stop_words.STOP_WORDS)

# Load the preprocessed data
df = pd.read_json('Data_Extraction_and_processing/extracted_text.json')

# Create a TfidfVectorizer object
vectorizer = TfidfVectorizer(stop_words='english')
vectorizer.fit_transform(df['extracted_portion'])
print(vectorizer)

# Define a function to generate a summary based on the user input
def generate_summary(user_input):
    cleaned_input = user_input
    input_vector = vectorizer.transform([cleaned_input])
    similarities = cosine_similarity(input_vector, vectorizer.transform(df['extracted_portion']))
    best_match_index = np.argmax(similarities)
    summary = df.loc[best_match_index, 'extracted_portion']
    score = similarities[0, best_match_index]
    return summary, score

def generate_response(prompt):
  GOOGLE_API_KEY= os.getenv('GOOGLE_API_KEY')
  genai.configure(api_key=GOOGLE_API_KEY)
  model = genai.GenerativeModel('gemini-1.5-flash')
  response = model.generate_content(prompt)
  return response.text



# Define a function to handle user input and generate a response
def handle_user_input(user_input):
    summary, score = generate_summary(user_input)  
    response = generate_response(user_input)
    return summary, score, response

def calculate_rouge(reference, hypothesis):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)
    return scores

def main():
  print("Hi! I'm your conversational AI Assistant and Text summarization bot, How can i help you today?")
  while True:
    user_input = input("Ask a question (or type 'exit' to quit): ")
    if user_input.lower() == "exit":
      break
    summary, score, response = handle_user_input(user_input)
    if score>0:
        rouge_scores = calculate_rouge(user_input, summary)
        print(f"Chatbot: {summary} \n\nSummary score: {score} \n\nRogue scores: {rouge_scores}")
    else:
        print(f"Chatbot: {response}")

if __name__ == "__main__":
  main()