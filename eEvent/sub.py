#!/usr/bin/env python
import csv
import datetime
import os
import pytz
import yagmail
from decimal import Decimal
from dotenv import load_dotenv
from typing import Optional
from google.cloud import pubsub_v1

from eEvent import env
from eEvent.auth import pgClient

load_dotenv(env)

EMAIL = os.getenv('EMAIL')
TIMEOUT = os.getenv('TIMEOUT')
PROJECT_ID = os.getenv('PROJECT_ID')
SUB_ID = os.getenv('SUB_ID')


def sub(
        eProjectId: str,
        eSubId: str,
        timeout: Optional[float] = None
) -> None:
    subscriber = pubsub_v1.SubscriberClient()
    eSubPath = subscriber.subscription_path(eProjectId, eSubId)

    def eCallBack(
            eMessage: pubsub_v1.subscriber.message.Message
    ) -> None:
        eThreads = pgClient.users().threads().list(
            userId='me').execute().get('threads', [])
        file = open("gmail.csv", "w", newline='')
        for thread in eThreads:
            # todo if thread['id'] in 'db' skip proc
            timestamp = None
            if len(thread['messages']) > 1 and \
                    os.path.isfile('gmail.csv'):
                writer = csv.writer(file)
                writer.writerow(["ID", "MEAN TIME"])
                writer.writerow([
                    thread['messages'][0]['id'],
                    Decimal('0.00')
                ])
                prev = None
                for message in thread['messages']:
                    if message['id'] == thread['id']:
                        timestamp = prev = message['internalDate']
                        continue
                    if timestamp:
                        mean = Decimal(
                            str(round(
                                ((message['internalDate']-timestamp)
                                 +
                                 (message['internalDate'] -
                                  prev)) / 2, 2))
                        )
                        writer.writerow([
                            message['id'], mean
                        ])
                    prev = message['internalDate']
                writer.writerow(['', ''])
        yagmail.SMTP(EMAIL).send(
            to=EMAIL,
            subject=f"eResponse Datasets on "
                    f"{datetime.datetime.now(tz=pytz.UTC)}",
            contents=f"A new batch of threads on "
                     f"{datetime.datetime.now(tz=pytz.UTC)}",
            attachments=file
        )
        file.close()
        eMessage.ack()
    future = subscriber.subscribe(eSubPath, callback=eCallBack)
    print(f"Listening for messages on {eSubPath}..\n")
    try:
        future.result(timeout=timeout)
    except: # noqa
        future.cancel()
        future.result()
    subscriber.close()


if __name__ == '__main__':
    TIMEOUT = TIMEOUT if TIMEOUT else None
    sub(PROJECT_ID, SUB_ID, TIMEOUT)
