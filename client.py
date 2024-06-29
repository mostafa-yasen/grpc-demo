import grpc

import helloworld_pb2
import helloworld_pb2_grpc

def run():
    with open("server.crt", "rb") as f:
        trusted_certs = f.read()

    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)

    with grpc.secure_channel("localhost:8000", credentials) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)

        metadata = [('authorization', 'valid-token')]

        # Unary call
        response = stub.SayHello(helloworld_pb2.HelloRequest(name="World"), metadata=metadata)
        print('Greeter client received: ' + response.message)


        # Client-side streaming call
        def generate_requests():
            for name in ["Alice", "Bob", "Charlie"]:
                yield helloworld_pb2.HelloRequest(name=name)

        response = stub.SayHelloClientStreaming(generate_requests(), metadata=metadata)
        print('Greeter client received: ' + response.message)

        # Server-side streaming call
        responses = stub.SayHelloServerStreaming(helloworld_pb2.HelloRequest(name="World"), metadata=metadata)
        for response in responses:
            print('Greeter client received: ' + response.message)


        # Bidirectional streaming call
        responses = stub.SayHelloBidirectionalStreaming(generate_requests(), metadata=metadata)
        for response in responses:
            print('Greeter client received: ' + response.message)



if __name__ == "__main__":
    run()
