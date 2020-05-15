#!/usr/bin/env python

import pika

# Establishing connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

"""
queue_declare is idempotent:
    - if the queue exists, it does nothing.
    - if the queue does not exist, it creates the queue.
We need to make sure the queue exists...
receive.py could be executed before send.py 
"""
channel.queue_declare(queue='q1')


def callback(ch, method, properties, body):
    """When we receive a message, this function is called."""
    print(" [x] Received %r" % body)


# Define what to do when consuming
channel.basic_consume(queue="q1",
                      auto_ack=True,
                      on_message_callback=callback)

# Never-ending loop that waits for data and runs callbacks whenever necessary
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
