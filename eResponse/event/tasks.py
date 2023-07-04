import os
import celery
from eResponse.celery import app
from eResponse.event.auth import service
from eResponse.event.models import ThreadEvent, Role, LastEventToken
from google.cloud import pubsub_v1
from celery.schedules import crontab
from django.db import transaction


@app.on_after_configure.connect
def renew_watch_service(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=0, hour=0), call_service.s())


@app.task
def call_service() -> None:
    publisher = pubsub_v1.PublisherClient()
    PID = os.getenv("PID")  # project_id
    TID = os.getenv("TID")  # topic_id
    tpath = publisher.topic_path(PID, TID)
    request = {'labelIds': ['INBOX'], 'topicName': tpath}
    # make actual call service.users.watch
    service.users().watch(userId='me', body=request).execute()


@celery.shared_task()
def complete_pubsub_task():
    if LastEventToken.objects.exists():
        token = LastEventToken.objects.last()
        latest_threads = service.users().threads().list(
            userId='me', includeSpamTrash=False, pageToken=token
        ).execute()
    else:
        latest_threads = service.users().threads().list(
            userId='me', includeSpamTrash=False
        ).execute()

    # cycle to the last page of threads
    token = None
    while 'nextPageToken' in latest_threads:
        token = latest_threads['nextPageToken']

        latest_threads = service.users().threads().list(
            userId='me', includeSpamTrash=False, pageToken=token
        ).execute()
    else:
        if token is not None:
            LastEventToken(token=token).save()

    # assert 'threads' in latest_threads
    if 'threads' in latest_threads:
        # atomic transaction favors credible db writes
        with transaction.atomic():
            # create threads from the list of threads in bulk
            events = [
                ThreadEvent.objects.create(id=thread['id'])
                if not ThreadEvent.objects.filter(id=thread['id']).exists()
                else ThreadEvent.objects.get(id=thread['id'])
                for thread in latest_threads['threads']
            ]
            # create roles for each thread in the list of messages in bulk
            for i, event in enumerate(events):
                thd = service.users().threads().get(
                    userId='me', id=event.id, format='minimal'
                ).execute()

                event.roles.add(*Role.objects.bulk_create([
                    Role(id=msg['id']) for msg in
                    thd['messages'][event.roles.all().count():]
                ]))
    return


def _run_process(threads: dict) -> None:
    pageToken = None

    # cycle to the last page of threads
    while 'nextPageToken' in threads:
        pageToken = threads['nextPageToken']

        threads = service.users().threads().list(
            userId='me', includeSpamTrash=False,
            pageToken=pageToken
        ).execute()

    # assert 'threads' in threads
    if 'threads' in threads:
        with transaction.atomic():

            events = [
                ThreadEvent.objects.create(id=thread['id'])
                if not ThreadEvent.objects.filter(id=thread['id']).exists()
                else ThreadEvent.objects.get(id=thread['id'])
                for thread in threads['threads']
            ]

            for i, event in enumerate(events):
                tred = service.users().threads().get(
                    userId='me', id=event.id, format='minimal'
                ).execute()

                event.roles.add(*Role.objects.bulk_create([
                    Role(id=msg['id']) for msg in
                    tred['messages'][len(event.roles.all()):]
                ]))

            if pageToken is not None:
                LastEventToken(token=pageToken).save()

    return


@celery.shared_task()
def ack_pubsub_message() -> None:
    last_event_token = LastEventToken.objects.filter()

    # starts from last known token subsequently
    if not last_event_token.exists():
        _run_process(service.users().threads().list(
            userId='me', includeSpamTrash=False
        ).execute())
    else:
        _run_process(service.users().threads().list(
            userId='me', includeSpamTrash=False,
            pageToken=last_event_token.last().token
        ).execute())
    return
