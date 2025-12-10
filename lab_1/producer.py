from confluent_kafka import Producer
conf = { 'bootstrap.servers': 'localhost:9094,localhost:9095' }

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


producer = Producer(conf)
for i in range(10):
    message = f'Hello Kafka {i}'
    print(f'Prodcue to dblab topic message: {message}')
    producer.produce('dblab', message.encode('utf-8'), callback=delivery_report)
    producer.poll(0) # Trigger delivery callback
producer.flush() # Wait for all messages to be delivered callback
