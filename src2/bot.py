from qa_model import QA_Model
from rl_model import RL_Model
from preprocessing import process_data

def main():
    # Process data
    segments = process_data('data/data.txt')
    
    print("Welcome to the Question-Answering Bot!")
    qa_model = QA_Model()  # Initialize QA model
    rl_model = RL_Model()  # Initialize RL model
    
    while True:
        # Prompt user for a question
        question = input("\nPlease enter your question (or type 'exit' to quit): ")
        
        # Check if user wants to exit
        if question.lower() == 'exit':
            print("Goodbye!")
            break
        
        # Use QA model to extract information
        answer = qa_model.answer_question(question, segments)
        
        # Use RL model to generate action based on QA output
        action = rl_model.predict_action(answer)
        
        # Display the answer
        print("\nAnswer:")
        print(answer)
        print("\nAction:")
        print(action)

if __name__ == "__main__":
    main()
