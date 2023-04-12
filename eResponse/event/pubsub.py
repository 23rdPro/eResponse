import os
from eResponse.event import service
from eResponse.event.tasks import ack_pubsub_message
from google.cloud import pubsub_v1


def callback(message: pubsub_v1.subscriber.message.Message):
    ack_pubsub_message.delay(message)
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
