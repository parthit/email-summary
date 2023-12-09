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
mail = imaplib.IMAP4_SSL("outlook.office365.com")


def get_last_email():
    # Login to your email account
    mail.login(email_address, password)

    # Select the mailbox (inbox in this case)
    mail.select("inbox")

    # Search for all emails and fetch the latest one
    result, data = mail.search(None, "ALL")
    latest_email_id = data[0].split()[-1]

    # Fetch the latest email
    result, message_data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = message_data[0][1]

    # Parse the raw email
    msg = email.message_from_bytes(raw_email)

    # Get the subject, sender, and body
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
                print('PLAIN TEXT')
            elif part.get_content_type() == "text/html":
                print('TEXT HTML')
                html_body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
                # print(body)
                soup = BeautifulSoup(html_body, 'html.parser')
                text_body += soup.get_text()
    else:
        # If the email is not multipart
        body = msg.get_payload()
        print(body)
        print('NOT MULTIPART')
        print(body)
        soup = BeautifulSoup(body, 'html.parser')
        text_body += soup.get_text()


    # Print the results
    print("Subject:", subject)
    print("Sender:", sender)
    # Logout from the email server
    print("Body:", text_body)
    mail.logout()

    return {'subject': subject, 'sender': sender, 'body': text_body}

