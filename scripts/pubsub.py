import json
import os
from django.db import transaction

from eResponse.event.models import ThreadEvent, Role
from google.cloud import pubsub_v1
from googleapiclient.errors import HttpError

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def _auth():
    SCOPES = ['https://www.googleapis.com/auth/cloud-platform',
              'https://mail.google.com/',
              'https://www.googleapis.com/auth/pubsub']
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


def callback(message: pubsub_v1.subscriber.message.Message):
    try:
        # messages are async
        # Queue.put(message) this is then handled by celery in another process todo

        decode = json.loads(message.data.decode('utf-8'))
        latest_thread = service.users().history().list(
            userId='me', startHistoryId=decode['historyId']
        ).execute()

        with transaction.atomic():
            event = ThreadEvent.objects.filter(
                id=latest_thread['historyId'])

            # list of message_history_modifying event
            history = latest_thread['history']

            roles = Role.objects.bulk_create([
                Role(id=msg['historyId'], role='2') for msg in history
                if msg['historyId'] != latest_thread['historyId']
                # separation of role -information managers
                # from information actors
            ])

            if not event.exists():
                event = ThreadEvent(id=latest_thread['historyId'])
                event.save()
                event.roles.add(*roles)
            else:
                event.get().roles.add(*roles)

        # threads_nextPageToken = threads['nextPageToken'] todo
        # str todo check(if nextPageToken) call next page

    except HttpError or Exception as error:
        print(f'Error:::::::>>>>>{error}')
    finally:
        message.ack()


def pubsub(timeout=100):
    # publisher code
    tpath = os.getenv('tpath')
    request = {'labelIds': ['INBOX'], 'topicName': tpath}

    # make actual call service.users.watch
    service.users().watch(userId='me', body=request).execute()
    # enabled gmail service to push to pubsub

    # subscriber code
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


def run():
    pubsub()
