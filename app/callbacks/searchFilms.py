from app.functions.packer import pack, unpack
from app.database import Connector
from pika import BasicProperties


def search_films_callback(ch, method, props, body, db: Connector):
    body: dict = unpack(body)
    response = {"state": "INVALID", "error": "UNKNOWN"}
    complete = False

    while not complete:
        if "query" not in body:
            response["error"] = "MISSING-FIELD"
            complete = True
            continue
        else:
            films = db.search_films(body["query"])
            if films:
                response = {
                    "state": "VALID",
                    "films": [f.dict for f in films]
                }
                complete = True
            else:
                response["error"] = "NOT-FOUND"
                complete = True

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=BasicProperties(correlation_id=props.correlation_id),
                     body=pack(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
