from confluent_kafka import Consumer, KafkaError
# use earliest to fetch all data and latest to fetch new data only
conf = { 'bootstrap.servers': 'localhost:9094,localhost:9095', 'group.id': 'hello', 'auto.offset.reset': 'earliest' }
consumer = Consumer(conf)
consumer.subscribe(['dblab'])
try:
    while True:
        msg = consumer.poll(1.0) # timeout in seconds
        if msg is None:
            # print('No message recieved')
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            break
        print(f"Received message: {msg.value().decode('utf-8')} from {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
except KeyboardInterrupt:
    print("Stopping consumer")
finally:
    consumer.close()
