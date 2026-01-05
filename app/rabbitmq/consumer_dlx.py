from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from datetime import datetime, timezone

connection_parameters = ConnectionParameters(
    host='localhost',
    port=5672,
    credentials=PlainCredentials(username='guest', password='guest')
)

def get_connection():
    return BlockingConnection(parameters=connection_parameters)

def processing_message(ch, method, properties, body: bytes):
    try:
        with open('./log_queue_message_dlx.txt', 'a') as f:
            f.write(f'{datetime.now(tz=timezone.utc).strftime('%d/%m/%Y, %H:%M:%S')} - {body.decode("utf-8")}\n')
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    with get_connection() as connection:
        with connection.channel() as channel:
            channel.exchange_declare(exchange_type='direct', exchange='dlx_exchange', durable=True)
            dlx_queue = channel.queue_declare(queue='dlx_queue', durable=True)
            channel.queue_bind(exchange='dlx_exchange', queue=dlx_queue.method.queue, routing_key='dlx_key')
            channel.basic_consume(queue=dlx_queue.method.queue, auto_ack=False, on_message_callback=processing_message)
            channel.start_consuming()

if __name__ == "__main__":
    main()