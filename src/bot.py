from summarization import tfidf_summarization
from preprocessing import process_data
from nltk.tokenize import sent_tokenize


def answer_question(question, segments):
    # Search for relevant segment containing the answer
    relevant_segment = None
    for segment in segments:
        if question.lower() in segment.lower():
            relevant_segment = segment
            break
    
    # If relevant segment found, summarize it
    if relevant_segment:
        summary = tfidf_summarization(relevant_segment, num_sentences=3)
    else:
        summary = "I'm sorry, I couldn't find the answer to your question."
    
    return summary
def main():
    # Process data
    segments = process_data('data/data.txt')
    
    print("Welcome to the Question-Answering Bot!")
    while True:
        # Prompt user for a question
        question = input("\nPlease enter your question (or type 'exit' to quit): ")
        
        # Check if user wants to exit
        if question.lower() == 'exit':
            print("Goodbye!")
            break
        
        # Answer the question
        answer = answer_question(question, segments)
        
        # Display the answer
        print("\nAnswer:")
        print(answer)

if __name__ == "__main__":
    main()