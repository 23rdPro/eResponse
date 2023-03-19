#!/usr/bin/env python
import hashlib
import os
import pathlib
import re
import socket
import sys

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from urllib.parse import unquote

load_dotenv('../.env')

REDIRECT = os.getenv('REDIRECT')
SERVER = os.getenv('SERVER')
PORT = int(os.getenv('PORT'))


def parse_raw_query_params(data) -> dict:
    decoded = data.decode("utf-8")
    match = re.search("GET\s\/\?(.*) ", decoded)
    params = match.group(1)
    pairs = [pair.split("=") for pair in params.split("&")]
    return {key: val for key, val in pairs}


def get_authorization_code(token: str) -> str:
    """
    :param token:
    :return:
    """
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((SERVER, PORT))
    sock.listen(1)
    connection, address = sock.accept()
    data = connection.recv(1024)
    params = parse_raw_query_params(data)
    message = None
    try:
        if not params.get('code'):
            error = params.get("error")
            message = f"Failed to retrieve authorization code. Error: {error}"
            raise ValueError(message)
        elif params.get("state") != token:
            message = "State token does not match the expected state."
            raise ValueError(message)
        else:
            message = "Authorization code was successfully retrieved."
    except ValueError as error:
        print(error)
        sys.exit(1)
    finally:
        response = (
            "HTTP/1.1 200 OK\n"
            "Content-Type: text/html\n\n"
            f"<b>{message}</b>"
            "<p>Please check the console output.</p>\n"
        )
        connection.sendall(response.encode())
        connection.close()
    return params.get("code")


def main(secpath: str, scopes: list) -> Credentials:
    """
    gapi client authorization flow for API requests
    :param secpath: secret path to json file
    :param scopes: list of scope address
    :return: google api service-build object
    """
    relpath = '../.secrets/token.json'
    cred: [Credentials] = Credentials

    if os.path.exists(relpath):
        cred = Credentials.from_authorized_user_file(relpath, scopes)

    elif not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())

        else:
            flow = Flow.from_client_secrets_file(secpath, scopes=scopes)
            flow.redirect_uri = REDIRECT
            token = hashlib.shake_256(os.urandom(1024)).hexdigest(8)
            auth_url, state = flow.authorization_url(
                access_type="offline",
                state=token,
                prompt="consent",
                include_granted_scopes="true",
            )
            print("Paste this URL into your browser: ")
            print(auth_url)
            print(f"\nWaiting for authorization and callback to: {REDIRECT}")
            code = unquote(get_authorization_code(token))
            flow.fetch_token(code=code)
            refresh_token = flow.credentials.refresh_token
            print(f"\nYour refresh token is: {refresh_token}\n")
            cred = flow.credentials

        with open(relpath, 'w') as token:
            token.write(cred.json())

    return cred


if __name__ == '__main__':
    seakret = os.getenv('AUTH_SECRET')
    SCOPES = ['https://mail.google.com/', ]
    abspath = (pathlib.Path(__file__).parent / seakret).resolve()
    get_cred = main(str(abspath), SCOPES)
    service = build('gmail', 'v1', credentials=get_cred)
