from lab_4 import rpc
from lab_4.grpc_files import cmd_pb2, cmd_pb2_grpc

import threading, subprocess, grpc
from concurrent import futures

class CommandServicer(cmd_pb2_grpc.CommandServicer):
    def SendCommand(self, request, context):
        print(subprocess.run(request.command, shell=True, capture_output=True, text=True, check=True).stdout)
        return cmd_pb2.Reply(msg="Command sending successfully")
    
def CmdServe():
    port = 50051
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cmd_pb2_grpc.add_CommandServicer_to_server(CommandServicer(), server)
    server.add_insecure_port(f"localhost:{port}")
    server.start()
    print(f"gRPC Command server running on localhost:{port}")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down...")


if __name__ == "__main__":
    SendMetricThread = threading.Thread(target=rpc.send_metric_data)
    SendMetricThread.start()
    CmdServerThread = threading.Thread(target=CmdServe)
    CmdServerThread.start()
    try:
        SendMetricThread.join()
        CmdServerThread.join()
    except KeyboardInterrupt:
        pass