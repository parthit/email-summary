from flask import Flask, request, jsonify
from services.llm import make_oai_call
from services.imap import get_last_email
import json
import threading

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, LLama Hack!'

@app.route('/summarize', methods=["GET"])
def summarize_email():
    if request.method == "GET":
        email_body = get_last_email()['body']
        response = make_oai_call(email_body, model="gpt-3.5-turbo-1106")
        return response

@app.route('/get_last_email', methods=["GET"])   
def get_last_received_email():
    if request.method == "GET":
        # Assuming you have a function named get_last_email to retrieve the last email
        last_email = get_last_email()

        if last_email:
            # You might want to format the last email data as needed
            subject = last_email['subject']
            sender = last_email['sender']
            body = last_email['body']

            # Return the last email data as JSON
            return jsonify({"subject": subject, "sender": sender, "body": body})
        else:
            return jsonify({"error": "No emails found."})

             

if __name__ == '__main__':
    app.run(debug=True)

