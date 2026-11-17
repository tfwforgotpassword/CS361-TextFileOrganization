# Text File Organizer Microservice

This microservice uses a text file to store a list of relations between currently-present text files within a folder.

## Requirements

Python 3.13

## How to Run

Keeping TextFileOrganization.txt and TextFileOrganization.py in the same folder:

First, run the TextFileOrganization.py file.
While it runs, run the client.py file.
From the client.py file, you can send one of four commands through text input via terminal.

`ListFiles` simply reads a list of all text files in the same folder.
`ListFileRelations` followed by a filename such as `Example1.txt` or `Example1` lists all text files recorded in TextFileOrganization text file as being related to that file.
`MakeFileRelation` followed by two filenames in either order, separated by a space, adds a relation to the TextFileOrganization file if it wasn't there previously.
Lastly, `Quit` terminates both client.py and TextFileOrganization.py.

`Examples:`
```
ListFiles
ListFileRelations Example1
ListFileRelations TextFileOrganization
MakeFileRelation TextFileOrganization Example1
Quit
```

The command is sent as a string to TextFileOrganization.py, which reads it to determine what to do.
In the first case (`ListFiles`) it checks the directory it is already in for text files.
For the next two, it consults the TextFileOrganization.txt file, which primarily stores relations in text format, one per line.
The format is `Example1.txt|Example2.txt` per line.
The last command simply ends the loop keeping the program running.

Afterwards, the client should receive another string, this one either a line-separated list of file names, or a simple confirmation
that the command was executed correctly.

`Standard outputs/replies:`
```
ListFiles

TextFileOrganization.txt
Example1.txt
Example2.txt
Unrelated.txt
```
```
ListFileRelations TextFileOrganization
Example1.txt
Example2.txt
```
```
MakeFileRelation TextFileOrganization Example1.txt

Relation added: Unrelated <-> Example1
```
```
Quit

Server shut down
```

`For various error cases:`
```
No relations for {file_name}
Text file not found: {file_name}
Relation added: {file_names[0]} <-> {file_names[1]}
Relation already exists: {file_names[0]} <-> {file_names[1]}
Invalid command
```

# UML

<img width="800" height="562" alt="image" src="https://i.imgur.com/VZL6dmp.png" />
