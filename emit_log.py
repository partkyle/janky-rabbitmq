#!/usr/bin/env python
import os
import sys

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.environ.get("RABBIT_HOST")))
channel = connection.channel()

channel.exchange_declare(exchange=os.environ.get('EXCHANGE_NAME'),
                         type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange=os.environ.get('EXCHANGE_NAME'),
                      routing_key='',
                      body=message)
print " [x] Sent %r" % (message,)
connection.close()