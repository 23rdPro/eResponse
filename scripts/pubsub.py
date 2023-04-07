import collections
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
        # gmservice.users().threads()
    except HttpError as error:
        print(":::::::>>>>>>auth", error)
        raise error
    finally:
        return gmservice


service = _auth()


def callback(message: pubsub_v1.subscriber.message.Message):

    def _bulk_create_role():
        # return Role.objects.bulk_create([
        #     Role(id=mess['historyId'], role='2') for mess in threads['messages']
        #     if mess['historyId'] != threads['historyId']
        # ])
        # return Role.objects.bulk_create([
        #     Role(id=)
        # ])
        # print(threads['messages'], '::::::;;;;:::;;;::><>mess')
        return Role.objects.bulk_create([
            Role(id=mess['historyId'], role='2') for mess in thread['messages']
            if mess['historyId'] != thread['historyId']
        ])

    try:
        # threads = service.users().threads().list(userId='me').execute().get('threads', [])
        # print(message, ':::::::::::::::::::>>>>>>>>>>>')
        decode = json.loads(message.data.decode('utf-8'))
        print(decode, ':::::::::;;;;;;decode>>>>>>')
        # our very own latest, newest threads
        threads = service.users().history().list(userId='me', startHistoryId=decode['historyId']).execute()
        history = threads['history']
        threads_nextPageToken = threads['nextPageToken']  # str todo check(if nextPageToken)
        # thread_queue = collections.deque()  # Queue()

        # for hist in history: todo



        # thread = service.users().threads().get(userId='me', startHistoryId=threads['historyId']).execute()
        print(threads, ':::::::::::::::::::>>>>>>>>>>>')

        with transaction.atomic():
            roles = _bulk_create_role()
            event = ThreadEvent.objects.filter(id=thread['historyId'])
            # event = ThreadEvent.objects.filter(id=threads['historyId'])  # or just id

            if event.exists():
                event.get().roles.add(*roles)
            else:
                event = ThreadEvent(id=thread['historyId'], role='1')
                event.save()
                event.roles.add(*roles)

    except HttpError or Exception as error:
        print(f'Error:::::::>>>>>{error}')
    finally:
        message.ack()


def pubsub(timeout=100):
    # publisher code

    publisher = pubsub_v1.PublisherClient()
    # tpath = publisher.topic_path(PID, TID)
    tpath = 'projects/eresponse/topics/eEvent'

    request = {'labelIds': ['INBOX'], 'topicName': tpath}
    # make actual call service.users.watch
    service.users().watch(userId='me', body=request).execute()
    # todo error maybe

    # subscriber code
    subscriber = pubsub_v1.SubscriberClient()
    # spath = subscriber.subscription_path(PID, SID)
    spath = 'projects/eresponse/subscriptions/eEvent-sub'
    future = subscriber.subscribe(spath, callback=callback)
    print(f"Listening for messages on {spath}..\n")
    try:
        future.result(timeout=timeout)
    except TimeoutError or Exception as error:  # noqa
        future.cancel()
        future.result()
        print(f'Error:::::::::pubsub(timeout code)>>>>{error}')
    finally:
        subscriber.close()


def run():
    pubsub()
