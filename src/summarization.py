from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def tfidf_summarization(text, num_sentences=3):
    # Convert the text into sentences
    sentences = text.split('.')
    
    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    
    # Compute TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(sentences)
    
    # Compute TF-IDF scores for each word
    word_scores = vectorizer.idf_
    
    # Calculate sentence scores
    sentence_scores = []
    for sentence in sentences:
        score = 0
        for word in sentence.split():
            if word in vectorizer.vocabulary_:
                score += word_scores[vectorizer.vocabulary_[word]]
        sentence_scores.append(score)
    
    # Select top sentences based on scores
    top_sentence_indices = np.argsort(sentence_scores)[-num_sentences:]
    summary = [sentences[i] for i in top_sentence_indices]
    
    return ' '.join(summary)
