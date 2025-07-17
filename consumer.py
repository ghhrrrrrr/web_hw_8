import pika
from models import Contact
from mongoengine.fields import ObjectId
import time
import json
import db

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='queue1', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    print(f" [x] Received {message}")
    time.sleep(1)
    send_email()
    set_to_sent(message['id'])
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
def set_to_sent(id):
    Contact.objects(id=ObjectId(id)).update(set__is_sent=True)
    
    
def send_email():
    pass


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='queue1', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
