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
socket.setsockopt(zmq.RCVTIMEO, 10000)

socket.connect("tcp://localhost:5555")

while True:
    print("ListFiles, ListFileRelations <filename>, MakeFileRelation are valid commands.")
    string_to_send = input("Type something!")

    socket.send_string(string_to_send)

    try:
        message = socket.recv_string()
    except zmq.Again:
        print("Error")
        break

    print(message)
    if message.endswith("Server shut down"):
        print("Thank you for using DataStealer5000.")
        break