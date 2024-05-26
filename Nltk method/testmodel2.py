import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Load the text file
with open('data/data.txt', 'r', encoding='utf-8') as file:
	text = file.read()

# Split the text into sentences
sentences = sent_tokenize(text)

# Remove stop words and tokenize the sentences
stop_words = set(stopwords.words('english'))
keyword_sentences = []
for sentence in sentences:
	tokens = [word for word in word_tokenize(sentence.lower()) if word not in stop_words]
	keyword_sentences.append(' '.join(tokens))

# Create a table or array with the original sentences and keyword sentences
table = list(zip(sentences, keyword_sentences))

# Define a function to calculate the correlation score
def calculate_score(question, sentence):
	vectorizer = CountVectorizer()
	q_vector = vectorizer.fit_transform([question])
	s_vector = vectorizer.transform([sentence])
	score = cosine_similarity(q_vector, s_vector)[0][0]
	return score

# Define a function to answer the user's question
def answer_question(question):
	scores = []
	for sentence, keywords in table:
		score = calculate_score(question, keywords)
		scores.append((sentence, keywords, score))
	scores.sort(key=lambda x: x[2], reverse=True)
	top_3_sentences = scores[:3]

	return top_3_sentences

# Test the function
question = "How many years does it take to complete the Computer Science programme at Lagos State University?"
for i, (answer, keywords, score) in enumerate(answer_question(question)):
    print(f'{i+1}. {answer} - Score: {score}')