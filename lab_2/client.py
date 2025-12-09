import socket

import grpc
import time
import subprocess

import test_pb2
import test_pb2_grpc

def generate_metric_data():
    commands = [
        r"""free | awk '/^Mem:/ { printf("%.2f\n", $3/$2 * 100) }'""",
        """top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8}'""",
        """iostat -d -k 1 2 | awk 'NR>7 {read+=$3} END {print read}'""",
        """iostat -d -k 1 2 | awk 'NR>7 {write+=$4} END {print write}'""",
        """ifstat -i wlp0s20f3 1 1 | awk 'NR>2 {print $1}'""",
        """ifstat -i wlp0s20f3 1 1 | awk 'NR>2 {print $2}'"""
    ]
    metrics = [
        "Memory Usage",
        "CPU Usage",
        "Read IO Usage",
        "Write IO Usage",
        "Network In Usage",
        "Network Out Usage",
    ]
    for i in range(6):
        result = subprocess.run(commands[i], shell=True, capture_output=True, text=True, check=True)
        yield test_pb2.MetricData(
            hostname = socket.gethostname(),
            metric = metrics[i],
            value = result.stdout.strip(),
            time = str(time.ctime()),
        )
        time.sleep(0.5)

def streaming_example(stub):
    try:
        while True:
            stream = stub.TransmitData(generate_metric_data(), timeout=20.0)
            for msg in stream:
                print("Stream response:", msg.reply)

            time.sleep(5)
    except grpc.RpcError as e:
        print("Stream failed:", e.code(), e.details())

def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = test_pb2_grpc.MonitorStub(channel)
        streaming_example(stub)

if __name__ == "__main__":
    main()