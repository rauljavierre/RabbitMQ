#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Fanout exchange:  it just broadcasts all the messages it receives to all the queues it knows
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Creating queue with random name. exclusive=True to delete the queue when process get killed
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# A binding is a relationship between an exchange and a queue
# Binding the queue to the exchange
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
