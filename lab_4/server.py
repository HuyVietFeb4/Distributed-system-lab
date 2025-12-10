import grpc, subprocess

from lab_4.grpc_files import monitor_pb2, monitor_pb2_grpc

from lab_4.kafka_connection import *

from concurrent import futures

class MonitorServicer(monitor_pb2_grpc.MonitorServicer):
    def TransmitData(self, request_iterator, context):
        for request in request_iterator:
            print(f"[{request.time}] Received {request.metric}: {request.value}, from {request.hostname}")
        return monitor_pb2.MetricReply(reply="Received successful")
        
def serve():
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

if __name__ == "__main__":
    serve()