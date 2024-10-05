import nltk
from nltk import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


nltk.download('punkt')
nltk.download('punkt_tab')

# Function to load text from a .txt file
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Step 1: Calculate TF-IDF scores for each sentence
def calculate_tfidf(sentences):
    vectorizer = TfidfVectorizer(stop_words='english')
    sentence_vectors = vectorizer.fit_transform(sentences)
    return vectorizer, sentence_vectors

# Step 2: Rank sentences based on query keywords
def rank_sentences_by_keywords(vectorizer, sentence_vectors, query):
    query_vector = vectorizer.transform([query])  # Vectorize the query
    # Calculate cosine similarity between the query vector and each sentence vector
    similarity_scores = cosine_similarity(sentence_vectors, query_vector)
    return similarity_scores

# Step 3: Extract top-ranked sentences based on query
def extract_top_sentences(sentences, scores, top_n=3):
    sorted_indices = np.argsort(scores, axis=0)[::-1][:top_n].flatten()  # Sort by score, descending
    top_sentences = [sentences[i] for i in sorted_indices if scores[i] > 0]
    return " ".join(top_sentences)

# Main retrieval function based on user input
def retrieval_based_summary(file_path, query, top_n=3):
    # Load text from the .txt file
    text = load_text(file_path)
    
    # Tokenize sentences
    sentences = sent_tokenize(text)
    
    # Calculate TF-IDF
    vectorizer, sentence_vectors = calculate_tfidf(sentences)
    
    # Rank sentences based on query
    scores = rank_sentences_by_keywords(vectorizer, sentence_vectors, query)
    
    # Extract top sentences based on score
    summary = extract_top_sentences(sentences, scores, top_n)
    
    return summary if summary else "No relevant information found."

# Example usage with continuous loop
if __name__ == "__main__":
    # Fixed path to the .txt document (you can update this path)
    file_path = r"C:\Users\user\Desktop\Final Project\final-year-proj\project-file-ngrams\corrected_final.txt"
    
    print("Type your query or type 'exit' to quit:")
    
    # Continuous loop to accept queries
    while True:
        # Get user query input
        query = input("\nEnter your query: ")
        
        # Break the loop if the user types 'exit'
        if query.lower() == 'exit':
            print("Exiting the program.")
            break
        
        # Retrieve the most relevant sentences based on user query
        summary = retrieval_based_summary(file_path, query, top_n=3)
        
        print(summary)