from concurrent import futures

import time
import grpc
import helloworld_pb2
import helloworld_pb2_grpc

class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message=f"Hello, {request.name}!")
    
    def SayHelloClientStreaming(self, request_iterator, context):
        names = []
        for request in request_iterator:
            names.append(request.name)

        return helloworld_pb2.HelloReply(
            message="Hello, %s!" % ', '.join(names)
        )
    
    def SayHelloServerStreaming(self, request, context):
        for i in range(5):
            yield helloworld_pb2.HelloReply(
                message="Hello, %s! -- %d" % (request.name, i)
            )
            time.sleep(1)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server=server)
    server.add_insecure_port("[::]:8000")
    print("Server started at: localhost:8000")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
