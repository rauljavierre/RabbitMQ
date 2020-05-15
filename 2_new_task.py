#!/usr/bin/env python

import pika
import sys


"""
Establishing connection with RabbitMQ server (in localhost).
If we wanted to connect to a broker on a different machine we'd
specify its name or IP address here.
"""
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

"""
We need to make sure the recipient queue exists. If we send a
message to non-existing location, RabbitMQ will just drop the
message. So we create a "task_queue" queue to which the message
will be delivered.
"""
channel.queue_declare(queue='task_queue', durable=True)

"""
Sending the message <body> to the queue <routing_key>. To see
more of the attribute <exchange>, go to third tutorial
"""
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # make message persistent
                      ))
print(" [x] Sent %r" % message)

# It will print if send works
print(" [x] Sent 'Hello World!'")


"""
We need to make sure the network buffers were flushed and
our message was actually delivered to RabbitMQ. We can do
it with this instruction.
"""
connection.close()
