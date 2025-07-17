
# docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management
import pika
from models import Contact
import db
import faker
import json

fake = faker.Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='emal_mock', exchange_type='direct')
channel.queue_declare(queue='queue1', durable=True)
channel.queue_bind(exchange='emal_mock', queue='queue1')


def main():
    for i in range(20):
        contact = Contact(fullname=fake.name(), email=fake.email())
        contact.save()

        message = {
            "id": str(contact.id),
            "message": 'message to contacts' 
        }

        channel.basic_publish(
            exchange='emal_mock',
            routing_key='queue1',
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % message)
    connection.close()
    
    
if __name__ == '__main__':
    main()
