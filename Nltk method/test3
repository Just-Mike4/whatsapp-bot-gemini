import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, ne_chunk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# nltk.download('maxent_ne_chunker')
# nltk.download('words')

class QuestionAnalyzer:
	def __init__(self, filename):
		with open(filename, 'r', encoding='utf-8') as file:
			self.text = file.read()
		self.sentences = sent_tokenize(self.text)
		self.keyword_sentences = []
		self.table = []

	def analyze(self):
		stop_words = set(stopwords.words('english'))
		for sentence in self.sentences:
			tokens = [word for word in word_tokenize(sentence.lower()) if word not in stop_words]
			self.keyword_sentences.append(' '.join(tokens))
		self.table = list(zip(self.sentences, self.keyword_sentences))

	def calculate_score(self, question, sentence):
		vectorizer = CountVectorizer()
		q_vector = vectorizer.fit_transform([question])
		s_vector = vectorizer.transform([sentence])
		score = cosine_similarity(q_vector, s_vector)[0][0]
		return score

	def answer_question(self, question):
		scores = []
		for sentence, keywords in self.table:
			score = self.calculate_score(question, keywords)
			scores.append((sentence, keywords, score))
		scores.sort(key=lambda x: x[2], reverse=True)
		top_3_sentences = scores[:1]

		# Word-by-word analysis and POS tagging
		words = word_tokenize(question)
		tagged_words = pos_tag(words)

		# Dependency parsing
		dependency_parse = ne_chunk(tagged_words)

		# Format the output
		answer = top_3_sentences[0][0] + ' - ' + str(top_3_sentences[0][2])
		return answer

# Test the code
filename = 'data/data.txt'  # replace with your .txt file
analyzer = QuestionAnalyzer(filename)
analyzer.analyze()
question = "What is the course title of CSC 104?"
answer = analyzer.answer_question(question)
print(answer)