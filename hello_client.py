import grpc

import helloworld_pb2
import helloworld_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:8000") as channel:
        name = None
        stub = helloworld_pb2_grpc.GreeterStub(channel)

        while name.lower() != "exit":
            name = input("What is your name? ")

            if name.lower() == "exit":
                print("Bye!")
                break

            response = stub.SayHello(helloworld_pb2.HelloRequest(name=name))
            print(f"Greeter client received: {response.message}")

if __name__ == "__main__":
    run()
