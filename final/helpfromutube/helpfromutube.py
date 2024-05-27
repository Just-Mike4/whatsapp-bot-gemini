import json
from difflib import get_close_matches

def load_knowledge_base(filepath: str) -> dict:
    with open(filepath, 'r') as file:
        data: dict = json.load(file)
        return data
    
def save_knowledge_base(data: dict, filepath: str):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]):
    matches: list = get_close_matches(user_question, questions,n=1,cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question:str, knowledge_base:dict):
    for q in knowledge_base['questions']:
        if q['question'] == question:
            return q["answer"]
        
def chat_bot():
    knowledge_base: dict = load_knowledge_base('final/helpfromutube/knowledgebase.json')

    while True:
        user_input : str = input("You: ")

        if user_input.lower() == 'quit':
            break

        best_match: str | None = find_best_match(user_input,[q['question'] for q in knowledge_base['questions']])

        if best_match:
            answer: str = get_answer_for_question(best_match,knowledge_base)
            print(f"Bot: {answer}")
        else:
            print("Bot: I am sorry, I do not understand that. Can you teach me?")
            new_answer: str = input("Type the answer or 'skip' to skip:")

            if new_answer.lower() != 'skip':
                knowledge_base['questions'].append({'question':user_input,'answer':new_answer})
                save_knowledge_base(knowledge_base,'final/helpfromutube/knowledgebase.json')
                print("Bot: Thanks for teaching me!")

if __name__ == '__main__':
    chat_bot()