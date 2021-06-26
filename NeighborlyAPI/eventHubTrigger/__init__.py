import json
import logging

import azure.functions as func


def main(event: func.EventHubEvent):
    body = event.get_body().decode()
    logging.info(f"Function triggered to process a message: {body}")
    logging.info(f"  EnqueuedTimeUtc = {event.enqueued_time}")
    logging.info(f"  SequenceNumber = {event.sequence_number}")
    logging.info(f"  Offset = {event.offset}")

    result = json.loads(body)
    logging.info("Python EventGrid trigger processed an event: {}".format(result))

    # Metadata
    for key in event.metadata:
        logging.info(f"Metadata: {key} = {event.metadata[key]}")
