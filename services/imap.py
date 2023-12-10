import imaplib
import email
import os
from email.header import decode_header
from datetime import datetime
import time
import threading
from bs4 import BeautifulSoup 

# Set your email and password
email_address = os.environ["PERSONAL_EMAIL"]
password = os.environ["EMAIL_PWD"]

# Connect to the mail server



def get_last_email():
    outlook_server = imaplib.IMAP4_SSL("outlook.office365.com")
    # Login to your email account
    outlook_server.login(email_address, password)

    # Select the mailbox (inbox in this case)
    outlook_server.select("inbox")

    # Search for all emails and fetch the latest one
    result, data = outlook_server.search(None, "ALL")
    latest_email_id = data[0].split()[-1]

    # Fetch the latest email
    result, message_data = outlook_server.fetch(latest_email_id, "(RFC822)")
    raw_email = message_data[0][1]

    # Parse the raw email
    msg = email.message_from_bytes(raw_email)

    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")

    sender, encoding = decode_header(msg.get("From"))[0]
    if isinstance(sender, bytes):
        sender = sender.decode(encoding or "utf-8")

    text_body = ""
    if msg.is_multipart():
        # If the email is multipart (contains both text and HTML parts)
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                text_body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
                soup = BeautifulSoup(html_body, 'html.parser')
                text_body += soup.get_text()
    else:
        # If the email is not multipart
        body = msg.get_payload()
        soup = BeautifulSoup(body, 'html.parser')
        text_body += soup.get_text()


    # Print the results
    print("Subject:", subject)
    print("Sender:", sender)
    # Logout from the email server
    print("Body:", text_body)
    outlook_server.logout()

    return {'subject': subject, 'sender': sender, 'body': text_body}

def check_for_new_emails(username=email_address, password=password, mailbox='inbox'):
    try:
        outlook_server = imaplib.IMAP4_SSL("outlook.office365.com")
        outlook_server.login(username, password)
        outlook_server.select(mailbox)

        print('Checking for new email')

        # Search for unseen emails
        status, messages = outlook_server.search(None, 'UNSEEN')

        if len(messages) == 0:
            print('No new emails to check')
        email_ids = messages[0].split()

        # If there are unseen emails, fetch and process the latest one
        if email_ids:
            latest_email_id = email_ids[-1]  # Get the latest unseen email
            status, msg_data = outlook_server.fetch(latest_email_id, '(RFC822)')

            # Parse the email content
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            sender, encoding = decode_header(msg.get("From"))[0]
            if isinstance(sender, bytes):
                sender = sender.decode(encoding or "utf-8")

            text_body = ""
            if msg.is_multipart():
                # If the email is multipart (contains both text and HTML parts)
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        text_body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
                    elif part.get_content_type() == "text/html":
                        html_body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
                        soup = BeautifulSoup(html_body, 'html.parser')
                        text_body += soup.get_text()
            else:
                # If the email is not multipart
                body = msg.get_payload()
                soup = BeautifulSoup(body, 'html.parser')
                text_body += soup.get_text()

            # Return the details of the last unseen email
            last_email = {'subject': subject, 'sender': sender, 'body': text_body}

        else:
            # No unseen emails found
            last_email = None

        # Logout from the Outlook IMAP server
        outlook_server.logout()
        print(last_email)
        return last_email

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
