import smtplib
from email.mime.text import MIMEText
import os

# Replace these with your SMTP server and authentication details
smtp_server = 'smtp-mail.outlook.com'
smtp_port = 587
smtp_username = os.environ["PERSONAL_EMAIL"]
smtp_password = os.environ["EMAIL_PWD"]

def send_summarized_email(subject='Test', summary='This is the summary', email_body="A very long email body"):
    # Create the email message
    subject = subject
    body = summary
    sender = smtp_username
    recipient = smtp_username

    message = MIMEText(body + "\n\n" + "_"*30 +'\nOrginal Email is Below\n'+ "_"*30 + '\n\n' + email_body)
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = recipient

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Start TLS if using a secure connection
        server.starttls()

        # Login to the SMTP server
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender, recipient, message.as_string())

    return "Email sent successfully."
