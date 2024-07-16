import os
import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

WEBHOOK_VERIFY_TOKEN = "140117" #os.getenv('WEBHOOK_VERIFY_TOKEN')
GRAPH_API_TOKEN ="EAAFeNWJxaA4BOyUBxiHqolXJqkiwh0oOlK7x7KdzqXWqhCotlWtrC4gZBDEUm0ZB59OPa1usJGb8XhDwnPyLGLh9wMMsX5DNL4EUfcgq9dySjtNfBGF0QNUkoD2SwHFQPQZCN7FHZAXW0U5th3HPobQurj7PKmk97NjTtZAyXNYI1iIO4qyRdE9F0C5CHpD0oBTbuZAdFlU0QysMpMcBEZD" #os.getenv('GRAPH_API_TOKEN')
PORT = int(os.getenv('PORT', 5000))

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Incoming webhook message:", json.dumps(data, indent=2))

    message = data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}).get('messages', [{}])[0]

    if message.get('type') == 'text':
        business_phone_number_id = data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}).get('metadata', {}).get('phone_number_id')
        reply_message_url = f'https://graph.facebook.com/v18.0/{business_phone_number_id}/messages'

        headers = {
            'Authorization': f'Bearer {GRAPH_API_TOKEN}',
        }
        message_data = {
            'messaging_product': 'whatsapp',
            'to': message.get('from'),
            'text': {'body': 'Echo: ' + message.get('text', {}).get('body')},
            'context': {
                'message_id': message.get('id'),
            },
        }

        # Send reply message
        requests.post(reply_message_url, headers=headers, json=message_data)

        # Mark message as read
        mark_read_data = {
            'messaging_product': 'whatsapp',
            'status': 'read',
            'message_id': message.get('id'),
        }
        requests.post(reply_message_url, headers=headers, json=mark_read_data)

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