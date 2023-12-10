from flask import Flask, request, jsonify
from services.llm import make_oai_call
from services.imap import get_last_email, check_for_new_emails
from services.outlook_smtp import send_summarized_email
import json
import threading
import time

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, LLama Hack!'

@app.route('/send_email', methods=["GET"])
def send_summarized_email():
    if request.method == "GET":
        email_body = get_last_email()['body']
        summarized_email_response = make_oai_call(email_body, model="gpt-3.5-turbo-1106")
        summarized_email_response = json.loads(summarized_email_response)

        subject = summarized_email_response['subject']
        body = summarized_email_response['body']
        response = send_summarized_email(subject=subject, summary=body, email_body=email_body)

        return response

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


# Create a global variable to store the last received email
last_received_email = {}

# Define a function to periodically check for new emails in a separate thread
def email_check_thread():
    global last_received_email
    while True:
        try:
            # Use the check_for_new_emails function to get the latest email
            last_received_email = check_for_new_emails()
        except Exception as e:
            print(f"An error occurred during email checking: {e}")

        # Sleep for 30 seconds before checking for new emails again
        time.sleep(30)

# Start the email-checking thread when the application starts
email_thread = threading.Thread(target=email_check_thread)
email_thread.daemon = True  # Allow the thread to be terminated when the main program exits
email_thread.start()


             

if __name__ == '__main__':
    app.run(debug=True)

