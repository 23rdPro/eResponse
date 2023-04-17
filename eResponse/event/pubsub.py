import os
from eResponse.event.auth import service
from eResponse.event import tasks
from google.cloud import pubsub_v1


def pubsub(timeout=None):

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
