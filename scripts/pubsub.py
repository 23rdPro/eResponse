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
    print(os.path.exists('application_default_credentials.json'), '::::::;KKKKK')
    SCOPES = ['mail', ]
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
        return Role.objects.bulk_create([
            Role(id=mess['historyId'], role='2') for mess in thread['messages']
            if mess['historyId'] != thread['historyId']
        ])

    try:
        # threads = service.users().threads().list(userId='me').execute().get('threads', [])
        print(message, ':::::::::::::::::::>>>>>>>>>>>')
        thread = service.users().threads().get(userId='me', id=message['historyId']).execute()

        with transaction.atomic():
            event = ThreadEvent.objects.filter(id=thread['historyId'])  # or just id
            roles = _bulk_create_role()

            if event.exists():
                event.get().roles.add(*roles)
            else:
                event = ThreadEvent(id=thread['historyId'], role='1')
                event.save()
                event.roles.add(*roles)

    except HttpError as error:
        print(f'Error:::::::>>>>>{error}')
    finally:
        message.ack()


def pubsub(timeout=None):
    # publisher code
    PID = os.getenv("PID")  # project_id
    TID = os.getenv("TID")  # topic_id -publisher
    SID = os.getenv("SID")

    publisher = pubsub_v1.PublisherClient()
    tpath = publisher.topic_path(PID, TID)

    request = {'labelIds': ['INBOX'], 'topicName': tpath}
    # make actual call service.users.watch
    service.users().watch(userId='me', body=request).execute()
    # todo error maybe

    # subscriber code
    subscriber = pubsub_v1.SubscriberClient()
    spath = subscriber.subscription_path(PID, SID)
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
