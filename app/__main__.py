from app.functions.env import EnvVars
from app.database import Connector
import pika

from app.callbacks import *

env_vars = EnvVars()  # Load in environment variables
# Message Broker--------
database = Connector(env_vars.mongo_uri, "notflix")
connection = pika.BlockingConnection(pika.connection.URLParameters(env_vars.mq_uri))  # Connect to message broker
channel = connection.channel()  # creates connection channel
# Define Queues and consumer
channel.queue_declare(queue="film-id")  # Declare Queue
channel.basic_consume(queue="film-id", on_message_callback=lambda ch, method, properties, body:
                      get_film_callback(ch, method, properties, body, database))
channel.queue_declare(queue="film-tag")  # Declare Queue
channel.basic_consume(queue="film-tag", on_message_callback=lambda ch, method, properties, body:
                      get_tag_films_callback(ch, method, properties, body, database))
channel.queue_declare(queue="film-cat")  # Declare Queue
channel.basic_consume(queue="film-cat", on_message_callback=lambda ch, method, properties, body:
                      get_category_films_callback(ch, method, properties, body, database))
channel.queue_declare(queue="film-all")  # Declare Queue
channel.basic_consume(queue="film-all", on_message_callback=lambda ch, method, properties, body:
                      get_all_films_callback(ch, method, properties, body, database))
channel.queue_declare(queue="film-search")  # Declare Queue
channel.basic_consume(queue="film-search", on_message_callback=lambda ch, method, properties, body:
                      search_films_callback(ch, method, properties, body, database))
# Start application consumer
channel.start_consuming()
connection.close()
