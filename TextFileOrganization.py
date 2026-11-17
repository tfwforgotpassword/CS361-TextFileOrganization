from time import sleep
import os
from pathlib import Path
import zmq
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
BASE = Path(__file__).resolve().parent
while True:
    message = socket.recv().decode()
    sleep(0.5)
    if message.startswith("ListFiles"):
        file_list = []
        for e in os.scandir(BASE):
            if e.is_file():
                with open(e.name, "r") as f:
                    if os.path.splitext(f.name)[1] == '.txt':
                        file_list.append(f.name)
        socket.send_string(str(file_list))
        message = ""
    if message.startswith("ListFileRelations"):
        if len(message) < 18:
            socket.send_string("Forgot file name")
        else:
            socket.send_string(message[18:])
        message = ""
    if message.startswith("Quit"):
        socket.send_string("Server shut down")
        break
    else:
        socket.send_string("Invalid command")
        message = ""
    sleep(0.5)