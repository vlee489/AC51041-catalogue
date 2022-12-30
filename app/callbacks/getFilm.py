from app.functions.packer import pack, unpack
from app.database import Connector
from pika import BasicProperties


def get_film_callback(ch, method, props, body, db: Connector):
    body: dict = unpack(body)
    response = {"state": "INVALID", "error": "UNKNOWN"}
    complete = False

    while not complete:
        if "id" not in body:
            response["error"] = "MISSING-FIELD"
            complete = True
            continue
        else:
            film = db.get_film_by_id(body["id"])
            if film:
                response = {
                    "state": "VALID",
                    "film": film.dict
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
