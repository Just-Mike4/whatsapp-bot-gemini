import random

# Define a list of possible user inputs and corresponding bot responses
user_inputs = [
    "Hi",
    "How are you?",
    "What's your name?",
    "Tell me a joke",
    "Goodbye"
]

bot_responses = [
    "Hello!",
    "I'm good, thanks for asking.",
    "My name is ChatBot.",
    "Why don't scientists trust atoms? Because they make up everything!",
    "Goodbye!"
]

# Define a function to generate a bot response based on user input
def generate_response(user_input):
    if user_input in user_inputs:
        index = user_inputs.index(user_input)
        return bot_responses[index]
    else:
        return "I'm sorry, I don't understand."

# Main loop to handle user input and generate bot responses
while True:
    user_input = input("You: ")
    response = generate_response(user_input)
    print("Bot: " + response)
    if response == "Goodbye!":
        break