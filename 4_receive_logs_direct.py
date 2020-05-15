#!/usr/bin/env python
import pika
import sys


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# Creating queue with random name. exclusive=True to delete the queue when process get killed
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# If we want to save only 'warning' and 'error' (and not 'info') log messages to a file
# python3.8 4_receive_logs_direct.py warning error > logs_from_rabbit.log
severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    # Binding the queue to the exchange with all the severities passed as argument
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
