from time import sleep
from pathlib import Path
import zmq
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
BASE = Path(__file__).resolve().parent


def get_file_relations(file_name):
    if not file_name.lower().endswith(".txt"):
        file_name += ".txt"

    related_files = {}
    reading_relations = False

    with (BASE / "TextFileOrganization.txt").open(encoding="utf-8") as relations_file:
        for line_number, line in enumerate(relations_file, start=1):
            line = line.strip()
            if line == "RELATIONS*":
                reading_relations = True
                continue
            if not reading_relations or not line:
                continue

            relation = line.split("|", 1)
            if len(relation) != 2 or not relation[0].strip() or not relation[1].strip():
                raise ValueError(f"Invalid relation on line {line_number}")

            first_file, second_file = relation[0].strip(), relation[1].strip()
            if first_file.casefold() == file_name.casefold():
                related_files.setdefault(second_file.casefold(), second_file)
            elif second_file.casefold() == file_name.casefold():
                related_files.setdefault(first_file.casefold(), first_file)

    return sorted(related_files.values(), key=str.casefold)


message = 0
while True:
    if type(message) != str or message == "":
        message = socket.recv().decode()
    sleep(0.5)
    if message.startswith("ListFiles"):
        file_list = []
        for file in BASE.iterdir():
            if file.is_file() and file.suffix.lower() == ".txt":
                file_list.append(file.name)
        file_list.sort(key=str.casefold)
        response = "\n" + "".join(f"{file_name}\n" for file_name in file_list)
        socket.send_string(response)
        message = ""
    if message == "ListFileRelations" or message.startswith("ListFileRelations "):
        file_name = message[len("ListFileRelations"):].strip()
        if not file_name:
            socket.send_string("Usage: ListFileRelations <filename>")
        else:
            try:
                related_files = get_file_relations(file_name)
            except ValueError as error:
                socket.send_string(str(error))
            else:
                response = "\n" + "".join(f"{related_file}\n" for related_file in related_files)
                socket.send_string(response)
        message = ""
    if message.startswith("Quit"):
        socket.send_string("Server shut down")
        break
    elif message != "":
        socket.send_string("Invalid command")
        message = ""
    sleep(0.5)