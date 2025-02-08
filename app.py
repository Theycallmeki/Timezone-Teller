from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv
from chatbot import get_time_in_country, generate_response

load_dotenv()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    # Check if input is a country to get time
    time_response = get_time_in_country(user_message)
    if "The current time in" in time_response:
        return jsonify({"response": time_response})
    
    # Otherwise, get a chatbot response
    chatbot_response = generate_response(user_message)
    return jsonify({"response": chatbot_response})

if __name__ == '__main__':
    app.run(debug=True)
