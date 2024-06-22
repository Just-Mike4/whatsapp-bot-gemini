import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def generate_response(prompt):
  GOOGLE_API_KEY= os.getenv('GOOGLE_API_KEY')
  genai.configure(api_key=GOOGLE_API_KEY)
  model = genai.GenerativeModel('gemini-1.5-flash')
  response = model.generate_content(prompt)
  return response.text

def main():
  print("Hi! I'm your conversational AI Assistant and Text summarization bot, How can i help you today?")
  while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
      break
    response_text = generate_response(user_input)
    print(f"Gemini: {response_text}")

if __name__ == "__main__":
  main()