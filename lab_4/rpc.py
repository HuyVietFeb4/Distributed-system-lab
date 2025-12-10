import grpc, time
from lab_4.grpc_files import monitor_pb2, monitor_pb2_grpc

from lab_4.collect import generate_metric_data
from lab_4 import config

def receive_data():
    results = generate_metric_data()
    for i in range(6):
        yield monitor_pb2.MetricData(
            hostname = config.HOST,
            metric = config.METRICS[i],
            value = results[config.METRICS[i]],
            time = str(time.ctime()),
        )

def send_metric_data():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = monitor_pb2_grpc.MonitorStub(channel)
        try:
            while True:
                
                response = stub.TransmitData(receive_data(), timeout=20.0)
                print(response.reply)
                time.sleep(10)

        except grpc.RpcError as e:
            print("Stream failed:", e.code(), e.details())