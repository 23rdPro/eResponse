import json
import os
import pprint

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
        # Queue.put(message), handled by celery in another process todo

        decode = json.loads(message.data.decode('utf-8'))
        latest_thread = service.users().history().list(
            userId='me', startHistoryId=decode['historyId']
        ).execute()

        if 'history' in latest_thread:

            history = latest_thread['history']

            with transaction.atomic():
                threads = ThreadEvent.objects.bulk_create([
                    ThreadEvent(id=item['messages'][0]['threadId'])
                    for item in history if not ThreadEvent.objects.filter(
                        id=item['messages'][0]['threadId']
                    ).exists])

                for i, thread in enumerate(threads):
                    assert history[i]['messages'][0]['threadId'] == thread.id

                    thread.roles.add(*Role.objects.bulk_create([
                        Role(id=msg['threadId'])
                        for msg in history[i]['messages'][len(thread.roles.all()):]
                    ]))

            # properly spread random events -statistics todo
        # threads_nextPageToken = threads['nextPageToken'] todo
        # str todo check(if nextPageToken) call next page

    except HttpError or Exception as error:
        print(f'Error:::::::>>>>>{error}')
    finally:
        message.ack()


def pubsub(timeout=None):
    # publisher code
    tpath = os.getenv('tpath')  # topic path
    request = {'labelIds': ['INBOX'], 'topicName': tpath}

    # make actual call service.users.watch
    service.users().watch(userId='me', body=request).execute()
    # enable gmail service to push to pubsub topic

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
