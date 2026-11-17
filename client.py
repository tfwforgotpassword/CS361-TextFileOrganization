# Client for ZeroMQ request-reply program. This will connect to
# a server via a request socket. Once connected to the localhost
# sends a string message and waits for reply from the server.
#
# This code was heavily based on the example found on
# zguide titled hwclient: https://zguide.zeromq.org/docs/chapter1/

import zmq

context = zmq.Context()

print("Client attempting to connect to server...")

socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5555")

while True:
    print(f"ListFiles, ListFileRelations, MakeFileRelation are valid commands.")
    string_to_send = input("Type something!")

    socket.send_string(string_to_send)

    message = socket.recv()
    
    print(f"Server sent back: {message.decode()}")
    if message.decode().endswith("Server shut down"):
        print("Thank you for using DataStealer5000.")
        break