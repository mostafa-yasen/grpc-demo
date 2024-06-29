from concurrent import futures

import time
import grpc
import helloworld_pb2
import helloworld_pb2_grpc
from auth_interceptor import AuthInterceptor


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

    def SayHelloBidirectionalStreaming(self, request_iterator, context):
        for request in request_iterator:
            yield helloworld_pb2.HelloReply(message=f"Hello, {request.name}")


# Import required libraries
import grpc
from concurrent import futures

def serve():
    # Create a gRPC server with ThreadPoolExecutor as its concurrency model.
    # max_workers=10 specifies the maximum number of threads that can be spawned to handle requests concurrently.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=[AuthInterceptor()])

    # Add a service to the server. Here, GreeterServicer is added.
    # GreeterServicer is a class generated from the protobuf file and it implements the rpc calls.
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    # Read the SSL key and certificate for secure communication
    # These files are used to establish a secure connection between the server and the client.
    with open("server.key", "rb") as f:
        private_key = f.read()
    with open("server.crt", "rb") as f:
        certificate_chain = f.read()

    # Create server credentials using the SSL key and certificate
    server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain),))

    # Add a secure port where the server will listen for requests.
    # The server is run on localhost and listens on port 8000.
    server.add_secure_port("[::]:8000", server_credentials)
    print("Server started at: localhost:8000")

    # Start the server
    server.start()

    # Keep the server running until it's explicitly stopped or until process termination
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
