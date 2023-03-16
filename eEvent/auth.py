#!/usr/bin/env python
import os
import pickle
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv('/Users/olumide/dev/eRS/src/.env')
SCOPES = ['https://mail.google.com/']
AUTH_SECRET = os.getenv('AUTH_SECRET')


def authenticate() -> build:
    """
    Authenticate Google API python client
    Google OAuth 2.0
    :return: googleapiclient.discovery.build
    """

    cred = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", 'rb') as token:
            cred = pickle.load(token)
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow. \
                from_client_secrets_file(AUTH_SECRET, SCOPES)
            cred = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(cred, token)
    return build('gmail', 'v1', credentials=cred)


pgClient = authenticate()  # python_gapi_client
