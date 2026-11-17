from time import sleep
from pathlib import Path
import shlex
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


def add_file_relation(first_file_name, second_file_name):
    def find_text_file(file_name):
        if not file_name.strip():
            raise ValueError("File name cannot be empty")
        if not file_name.lower().endswith(".txt"):
            file_name += ".txt"
        if Path(file_name).name != file_name:
            raise ValueError(f"Invalid file name: {file_name}")

        for file in BASE.iterdir():
            if file.is_file() and file.suffix.lower() == ".txt" and file.name.casefold() == file_name.casefold():
                return file.name
        raise ValueError(f"Text file not found: {file_name}")

    first_file = find_text_file(first_file_name)
    second_file = find_text_file(second_file_name)
    if first_file.casefold() == second_file.casefold():
        raise ValueError("A file cannot be related to itself")

    relations_path = BASE / "TextFileOrganization.txt"
    contents = relations_path.read_text(encoding="utf-8")
    if "RELATIONS*" not in contents.splitlines():
        raise ValueError("Relations section not found")

    if second_file.casefold() in {file.casefold() for file in get_file_relations(first_file)}:
        return False

    with relations_path.open("a", encoding="utf-8") as relations_file:
        if contents and not contents.endswith(("\n", "\r")):
            relations_file.write("\n")
        relations_file.write(f"{first_file}|{second_file}\n")
    return True


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
        if file_name.startswith(("'", '"')):
            try:
                parsed_file_names = shlex.split(file_name)
            except ValueError:
                parsed_file_names = []
            file_name = parsed_file_names[0] if len(parsed_file_names) == 1 else ""
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
    if message == "MakeFileRelation" or message.startswith("MakeFileRelation "):
        arguments = message[len("MakeFileRelation"):].strip()
        try:
            file_names = shlex.split(arguments)
        except ValueError:
            file_names = []

        if len(file_names) != 2:
            socket.send_string('Usage: MakeFileRelation <filename1> <filename2> (quote names containing spaces)')
        else:
            try:
                added = add_file_relation(file_names[0], file_names[1])
            except (OSError, ValueError) as error:
                socket.send_string(str(error))
            else:
                if added:
                    socket.send_string(f"Relation added: {file_names[0]} <-> {file_names[1]}")
                else:
                    socket.send_string(f"Relation already exists: {file_names[0]} <-> {file_names[1]}")
        message = ""
    if message.startswith("Quit"):
        socket.send_string("Server shut down")
        break
    elif message != "":
        socket.send_string("Invalid command")
        message = ""
    sleep(0.5)