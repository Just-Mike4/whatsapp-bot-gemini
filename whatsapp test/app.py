import logging
import os
import json
import re
import requests
import google.generativeai as genai
import spacy
import pandas as pd
import string
import numpy as np
import language_tool_python
from flask import Flask, request, jsonify, current_app
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

app = Flask(__name__)

WEBHOOK_VERIFY_TOKEN =os.getenv('WEBHOOK_VERIFY_TOKEN')
GRAPH_API_TOKEN = os.getenv('GRAPH_API_TOKEN')
PORT = int(os.getenv('PORT', 8000))

tool = language_tool_python.LanguageToolPublicAPI('en-US')
load_dotenv()

nlp = spacy.load('en_core_web_sm')
punc = string.punctuation
stopwords = list(spacy.lang.en.stop_words.STOP_WORDS)

df = pd.read_json(r'C:\Users\user\Desktop\Final Project\final-year-proj\Data_Extraction_and_processing\extracted_text.json')
vectorizer = TfidfVectorizer(stop_words='english')
vectorizer.fit_transform(df['extracted_portion'])

def generate_summary(user_input):
    cleaned_input = user_input
    input_vector = vectorizer.transform([cleaned_input])
    similarities = cosine_similarity(input_vector, vectorizer.transform(df['extracted_portion']))
    best_match_index = np.argmax(similarities)
    summary = df.loc[best_match_index, 'extracted_portion']
    score = similarities[0, best_match_index]
    return summary, score

def generate_response1(prompt):
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

def correct_grammar(text):
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text

def handle_user_input(user_input):
    summary, score = generate_summary(user_input)
    corrected_summary = correct_grammar(summary)
    response = generate_response1(user_input)
    return corrected_summary, score, response

def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")

def get_text_message_input(recipient, text):
    return json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient,
        "type": "text",
        "text": {"preview_url": False, "body": text},
    })

def generate_response(prompt):
    summary, score, response = handle_user_input(prompt)
    if score > 0:
        response = summary
    return response

def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {GRAPH_API_TOKEN}",
    }
    url = f"https://graph.facebook.com/v18.0/{current_app.config['PHONE_NUMBER_ID']}/messages"
    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except requests.RequestException as e:
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        log_http_response(response)
        return response

def process_text_for_whatsapp(text):
    text = re.sub(r"\【.*?\】", "", text).strip()
    text = re.sub(r"\*\*(.*?)\*\*", r"*\1*", text)
    return text

def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]
    response = generate_response(message_body)
    data = get_text_message_input(wa_id, response)
    send_message(data)

def is_valid_whatsapp_message(body):
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Incoming webhook message:", json.dumps(data, indent=2))
    if is_valid_whatsapp_message(data):
        process_whatsapp_message(data)
    return '', 200

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
        print("Webhook verified successfully!")
        return challenge, 200
    else:
        return 'Forbidden', 403

@app.route('/')
def index():
    return '<pre>Nothing to see here.\nCheckout README.md to start.</pre>'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)