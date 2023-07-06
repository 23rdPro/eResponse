import os
# import eResponse
# from eResponse.event.auth import service
from eResponse.event import tasks
from google.cloud import pubsub_v1


from googleapiclient.errors import HttpError

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def _auth():
    SCOPES = ['https://www.googleapis.com/auth/cloud-platform',
              'https://mail.google.com/',
              'https://www.googleapis.com/auth/pubsub'
              ]
    creds = None
    if os.path.exists('scripts/application_default_credentials.json'):
        creds = Credentials.from_authorized_user_file(
            'scripts/application_default_credentials.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'scripts/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('scripts/application_default_credentials.json', 'w') as token:
            token.write(creds.to_json())

    gmservice = None

    try:
        gmservice = build('gmail', 'v1', credentials=creds)
    except HttpError as error:
        print(error)
        # raise error
    finally:
        return gmservice


service = _auth()


def pubsub(timeout=None):
    """

    :param timeout:
    :return:
    """

    def callback(message: pubsub_v1.subscriber.message.Message):
        # decode = json.loads(message.data.decode('utf-8'))
        tasks.ack_pubsub_message.delay()
        message.ack()

    tpath = os.getenv('tpath')  # topic path
    request = {'labelIds': ['INBOX'], 'topicName': tpath}

    # make call with watch() to push to pubsub topic
    service.users().watch(userId='me', body=request).execute()

    subscriber = pubsub_v1.SubscriberClient()
    spath = os.getenv('spath')
    future = subscriber.subscribe(spath, callback=callback)
    print(f"Listening for messages on {spath}..\n")

    try:
        future.result(timeout=timeout)
    except TimeoutError or Exception as error:  # noqa
        future.cancel()
        future.result()
        print(f'Error:::::::::pubsub>>>>{error}')
    finally:
        subscriber.close()
