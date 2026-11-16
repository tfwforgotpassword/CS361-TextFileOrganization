from time import sleep
import os
while True:#ALTER THE BELOW TEXT TO FIT WITH THE PROGRAM IDEA, UI IS TEST FILE
    sleep(1.0)
    storage_service = open('TextFileOrganization.txt', 'r')
    store_service_result = storage_service.read(3)
    if store_service_result.startswith("run"):
        path = r"C:\Users\andth\Documents\cs361"
        for e in os.scandir(path):
            if e.is_file():
                with open(e.path, "r") as f:
                    print(f.name)
    sleep(10.0)#gotta do this later i guess
    storage_service.close()