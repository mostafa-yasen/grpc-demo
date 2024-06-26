import grpc

import helloworld_pb2
import helloworld_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:8000") as channel:
        name = None
        stub = helloworld_pb2_grpc.GreeterStub(channel)

        # Unary call
        response = stub.SayHello(helloworld_pb2.HelloRequest(name="World"))
        print('Greeter client received: ' + response.message)


        # Client-side streaming call
        def generate_requests():
            for name in ["Alice", "Bob", "Charlie"]:
                yield helloworld_pb2.HelloRequest(name=name)

        response = stub.SayHelloClientStreaming(generate_requests())
        print('Greeter client received: ' + response.message)

        # Server-side streaming call
        responses = stub.SayHelloServerStreaming(helloworld_pb2.HelloRequest(name="World"))
        for response in responses:
            print('Greeter client received: ' + response.message)


if __name__ == "__main__":
    run()
