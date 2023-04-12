import os
import json
import celery
from abc import ABC
from eResponse.celery import app
from eResponse.event.pubsub import service
from eResponse.event.models import ThreadEvent, Role
from google.cloud import pubsub_v1
from googleapiclient.errors import HttpError
from celery.schedules import crontab
from celery import shared_task
from django.db import transaction


@app.on_after_configure.connect
def renew_watch_service(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=0, hour=0), call_service.s())


@app.task
def call_service():
    publisher = pubsub_v1.PublisherClient()
    PID = os.getenv("PID")  # project_id
    TID = os.getenv("TID")  # topic_id
    tpath = publisher.topic_path(PID, TID)
    request = {'labelIds': ['INBOX'], 'topicName': tpath}
    # make actual call service.users.watch
    service.users().watch(userId='me', body=request).execute()


class BaseRetryTask(celery.Task, ABC):
    autoretry_for = (Exception, )
    retry_backoff = True
    retry_jitter = True
    retry_kwargs = {'max_retries': 5, 'countdown': 5}


@shared_task(bind=True, base=BaseRetryTask)
def ack_pubsub_message(message: pubsub_v1.subscriber.message.Message) -> None:
    decode = json.loads(message.data.decode('utf-8'))
    latest_change = None

    try:
        latest_change = service.users().history().list(
            userId='me', startHistoryId=decode['historyId']
        ).execute()

    except HttpError:
        raise HttpError

    if 'history' in latest_change:

        history = latest_change['history']

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
    return
