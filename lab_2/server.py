import time
import grpc

import test_pb2
import test_pb2_grpc

from concurrent import futures

class MonitorServicer(test_pb2_grpc.MonitorServicer):
    def TransmitData(self, request_iterator, context):
        for msg in request_iterator:
            yield test_pb2.MetricReply(reply=f"[{msg.time}] Received {msg.value} {msg.metric} from {msg.hostname}")
            time.sleep(0.3)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_MonitorServicer_to_server(MonitorServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server running on :50051")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    serve()