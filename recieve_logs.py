#!/usr/bin/env python
import os

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.environ.get('RABBIT_HOST')))
channel = connection.channel()

channel.exchange_declare(exchange=os.environ.get('EXCHANGE_NAME'),
                         type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange=os.environ.get('EXCHANGE_NAME'),
                   queue=queue_name)

print ' [*] Waiting for logs. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] %r" % (body,)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
