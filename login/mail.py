import os
import base64
import json
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from login_info import get_all_info


SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def authenticate_gmail_api():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def create_message(sender, to, subject, body):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(body)
    message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_email(creds, sender, to, subject, body):
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = create_message(sender, to, subject, body)
        send_message = service.users().messages().send(userId="me", body=message).execute()
        print(f"Message sent successfully: {send_message['id']}")
    except Exception as error:
        print(f"An error occurred: {error}")

def send_login_notification():
    creds = authenticate_gmail_api()

    sender_email = 'EMAIL OF PERSON SENDING EMAIL'
    recipient_email = 'EMAIL OF RECEIVER'
    subject = "Login Attempt Notification"
    mail_content = get_all_info()
    body = f"A login attempt has been made on your account.\nLOGIN INFO:\n{mail_content}"


    send_email(creds, sender_email, recipient_email, subject, body)


# send_login_notification()
