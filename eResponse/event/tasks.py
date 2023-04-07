from celery.schedules import crontab

# from celery.task import periodic_task


# service.users.watch()
from eResponse.celery import app
from eResponse.event.pubsub import service
from google.cloud import pubsub_v1
from celery.schedules import crontab
import os


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




