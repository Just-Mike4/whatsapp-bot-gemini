from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# New sample corpus
corpus = [
    "The cat sat on the mat.",
    "The dog sat on the mat.",
    "The cat chased the mouse."
]

# New user input
new_input = ["Where did the cat sit?"]

# Initialize TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words='english')

# Fit the vectorizer to the corpus
vectorizer.fit(corpus)

# Print the vocabulary and IDF values
vocabulary = vectorizer.vocabulary_
idf_values = vectorizer.idf_

# Transform the corpus
tfidf_matrix = vectorizer.transform(corpus)

# Transform the new user input
input_vector = vectorizer.transform(new_input)

# Compute cosine similarity between the new input and the corpus
similarities = cosine_similarity(input_vector, tfidf_matrix)

# Find the best match
best_match_index = np.argmax(similarities)
best_match_score = similarities[0, best_match_index]

# Display results
print("Vocabulary:", vocabulary)
print("IDF Values:", idf_values)
print("TF-IDF Matrix for Corpus:\n", tfidf_matrix.toarray())
print("TF-IDF Vector for User Input:\n", input_vector.toarray())
print("Cosine Similarities:\n", similarities)
print(f"Best Match Index: {best_match_index}")
print(f"Best Match Score: {best_match_score}")
print(f"Best Matching Document: {corpus[best_match_index]}")
