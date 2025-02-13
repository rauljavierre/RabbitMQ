#!/usr/bin/env python
import pika
import sys


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

# If we want to set multiple bindings...
# python3.8 5_receive_logs.topic.py "kern.*" "*.critical"
binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    # Binding the queue to the exchange with all the binding keys passed as argument
    channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)


print(' [*] Waiting for logs. To exit press CTRL+C')
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
