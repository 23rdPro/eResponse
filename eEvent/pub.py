#!/usr/bin/env python
import os

from google.cloud import pubsub_v1
from eEvent.auth import pgClient


def pub(eProjectId: str, eTopicId: str) -> None:
    """
    watch in real-time for mail inbox events,
    publish event to network,
    * handle new threads in subscriber callback
    :param eProjectId: emergency project_id
    :param eTopicId: emergency topic_id
    :return:
    """

    publisher = pubsub_v1.PublisherClient()
    eTopicPath = publisher.topic_path(eProjectId, eTopicId)
    eRequest = {'labelIds': ['INBOX'], 'topicName': eTopicPath}

    pgClient.users().watch(userId='me', body=eRequest).execute()


if __name__ == '__main__':
    from dotenv import load_dotenv
    from eEvent import env

    load_dotenv(env)

    PROJECT_ID = os.getenv('PROJECT_ID')
    TOPIC_ID = os.getenv('TOPIC_ID')

    pub(PROJECT_ID, TOPIC_ID)
