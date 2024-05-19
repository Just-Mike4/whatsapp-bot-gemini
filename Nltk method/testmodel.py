import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# nltk.download('punkt')
# nltk.download('stopwords')  
# nltk.download('wordnet')

# Read the text file
with open('data/data.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Tokenize the text into sentences
sentences = nltk.sent_tokenize(text)

# Tokenize the text into words and remove stopwords
stop_words = set(stopwords.words('english'))
word_tokens = [word_tokenize(sentence.lower()) for sentence in sentences]
filtered_sentences = [[word for word in tokens if word not in stop_words] for tokens in word_tokens]

# Lemmatize words
lemmatizer = WordNetLemmatizer()
lemmatized_sentences = [[lemmatizer.lemmatize(word) for word in filtered_sentence] for filtered_sentence in filtered_sentences]

# Create a table or array with original and preprocessed sentences
sentence_table = [{'original': sent, 'processed': ' '.join(lem_sent)} for sent, lem_sent in zip(sentences, lemmatized_sentences)]

# Vectorize the preprocessed sentences using TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([' '.join(lem_sent) for lem_sent in lemmatized_sentences])

# Function to preprocess user question
def preprocess_question(question):
    question_tokens = word_tokenize(question.lower())
    question_words = [word for word in question_tokens if word not in stop_words]
    lemmatized_question = [lemmatizer.lemmatize(word) for word in question_words]
    return ' '.join(lemmatized_question)

# Function to get top N relevant sentences to user question
def get_top_sentences(question, n=3):
    preprocessed_question = preprocess_question(question)
    question_vector = vectorizer.transform([preprocessed_question])
    similarity_scores = cosine_similarity(question_vector, tfidf_matrix)[0]
    top_indices = similarity_scores.argsort()[-n:][::-1]
    top_sentences = [(sentences[i], similarity_scores[i]) for i in top_indices if len(sentences[i].split()) > 7]
    return top_sentences

# Example usage
user_question = "What is the unit of CSC 104?"
top_sentences = get_top_sentences(user_question)
for i, (sentence, score) in enumerate(top_sentences):
    print(f"{i+1}. {sentence} (Score: {score:.3f})")
