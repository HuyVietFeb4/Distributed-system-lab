import grpc, subprocess
import json
from lab_4.grpc_files import monitor_pb2, monitor_pb2_grpc
import threading
from lab_4.kafka_connection import kafka_connection

from concurrent import futures

class MonitorServicer(monitor_pb2_grpc.MonitorServicer):
    def TransmitData(self, request_iterator, context):
        message = {} 
        for request in request_iterator:
            message[request.metric] = request.value
            print(f"[{request.time}] Received {request.metric}: {request.value}, from {request.hostname}")  
        kafka = kafka_connection('grpc_server')
        kafka.produce('monitor', json.dumps(message).encode('utf-8'))       
        return monitor_pb2.MetricReply(reply="Received successful")

        
def client_to_kafka():
    ip = subprocess.run("hostname -I", shell=True, capture_output=True, text=True, check=True).stdout.split(" ")[0]
    port = 50051
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    monitor_pb2_grpc.add_MonitorServicer_to_server(MonitorServicer(), server)
    server.add_insecure_port(f"localhost:{port}")
    server.start()
    print(f"gRPC server running on localhost:{port}")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down...")


def kafka_to_client():
    kafka = kafka_connection('grpc_server')
    kafka.consume('cmd')
    
if __name__ == "__main__":
    ck_thread = threading.Thread(target=client_to_kafka)
    kc_thread = threading.Thread(target=kafka_to_client)

    ck_thread.start()
    kc_thread.start()
    try:
        ck_thread.join()
        kc_thread.join()
    except KeyboardInterrupt:
        print('Server shutdown')