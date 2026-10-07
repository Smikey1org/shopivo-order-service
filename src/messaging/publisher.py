import json

import pika

from src.core.config import settings
from src.messaging.events import EXCHANGE_NAME


def publish_order_created(event: dict) -> None:
    connection = pika.BlockingConnection(
        pika.URLParameters(settings.rabbitmq_url)
    )

    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type="direct",
        durable=True,
    )

    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key="order.created",
        body=json.dumps(event),
    )

    connection.close()
