import pika
import rich
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.0.112', credentials=pika.PlainCredentials(username='user', password='password')))
channel = connection.channel()
rich.print(channel)


def put_message_to_rmq(queue_name:str, message:str):
	channel.queue_declare(queue=queue_name)
	channel.basic_publish(exchange='', routing_key=queue_name, body=message)
	print(f'Add message {message} into queue {queue_name}')

def callback_recieved_message(ch, method, properties, body:bytes):
    print(f"Received: '{body.decode(encoding='utf8',  errors='ignore')}', ch:{ch}, method:{method}, properties:{properties}")


if sys.argv[1]=='publish':
	put_message_to_rmq(sys.argv[2], sys.argv[3])


if sys.argv[1]=='subscribe':
	channel.basic_consume(sys.argv[2], on_message_callback=callback_recieved_message, auto_ack=True)
	print('Waiting for messages. To exit press CTRL+C')
	channel.start_consuming()


connection.close()