from transformers import pipeline

class QA_Model:
    def __init__(self):
        self.qa_model = pipeline("question-answering")

    def answer_question(self, question, segments):
        text = " ".join(segments)
        return self.qa_model(question=question, context=text)["answer"]
