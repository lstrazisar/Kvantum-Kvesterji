import pickle
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pathlib import Path


class GmailApi:
    def __init__(self) -> None:
        # Request all access (permission to read/send/receive emails, manage the inbox, and more)
        # our_email = 'conductor.h2020@gmail.com'
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        self.TOKEN_PATH = "token.pickle"
        self.CREDENTIALS_FILE = "credentials.json"
        self.service = self.__gmail_authenticate()


    def send_message(self, sender, receiver, subject, body):
        def build_message(sender, receiver, subject, body):
            if type(receiver) == list: receiver = ", ".join(receiver)
            message = MIMEText(body, _subtype='html')
            message['to'], message['from'], message['subject']  = receiver, sender, subject
            return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}
        
        def send(sender, receiver, subject, body):
            message = build_message(sender, receiver, subject, body)
            return self.service.users().messages().send(userId="me", body=message).execute()

        try:
            return send(sender, receiver, subject, body)
        except Exception as e:
            self.service = self.__gmail_authenticate()
            return send(sender, receiver, subject, body)
    

    def __gmail_authenticate(self):
        creds = self.__get_or_refresh_credentials()
        return build('gmail', 'v1', credentials=creds)
    

    def __get_or_refresh_credentials(self):
        # the file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        creds = None
        if Path(self.TOKEN_PATH).exists():
            with open(self.TOKEN_PATH, "rb") as token:
                creds = pickle.load(token)
        # if there are no (valid) credentials available, let the user log in.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(self.CREDENTIALS_FILE, self.SCOPES)
            creds = flow.run_local_server(open_browser=False, bind_addr="0.0.0.0", port=8080)
            with open(self.TOKEN_PATH, "wb") as token:
                pickle.dump(creds, token)
            
        return creds
