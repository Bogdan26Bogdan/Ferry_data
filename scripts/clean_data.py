import json
import os
import sys

def check_down(file_name: str) -> bool:
    with open(file_name, "r") as file:
        data = json.load(file)

    if "BC Ferries Data Currently Down" == data:
        return True
    return False


def remove_down_files(directory: str):
    for file in os.listdir(directory):
        if check_down(directory + file):
            os.remove(directory + file)


if __name__ == "__main__":
    remove_down_files(sys.argv[1])
