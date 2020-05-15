#!/usr/bin/env python

import pika


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
message. So we create a "q1" queue to which the message
will be delivered.
"""
channel.queue_declare(queue='q1')

"""
Sending the message <body> to the queue <routing_key>. To see
more of the attribute <exchange>, go to third tutorial
"""
channel.basic_publish(exchange='',
                      routing_key='q1',
                      body='Hello World!')

# It will print if send works
print(" [x] Sent 'Hello World!'")


"""
We need to make sure the network buffers were flushed and
our message was actually delivered to RabbitMQ. We can do
it with this instruction.
"""
connection.close()
