#!/usr/bin/env python

import pika
import time

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
channel.queue_declare(queue='task_queue', durable=True)


def callback(ch, method, properties, body):
    """When we receive a message, this function is called."""
    print(" [x] Received %r" % body)

    # We will fake a second of work for every dot in the message body
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Don't dispatch a new message to a worker until it has processed and acknowledged the previous one
# It ensures equitable work-queue
channel.basic_qos(prefetch_count=1)

# Define what to do when consuming
channel.basic_consume(queue="task_queue", on_message_callback=callback)

# Never-ending loop that waits for data and runs callbacks whenever necessary
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
