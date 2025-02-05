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


def files_have_same_data(file1: str, file2: str) -> bool:
    with open(file1, "r") as f1, open(file2, "r") as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
        return data1 == data2


def remove_duplicate_files(directory: str):
    """Remove files that contain exactly the same data as their chronological neighbor"""
    files = sorted(os.listdir(directory))
    
    # Compare each file with the next one chronologically
    i = 0
    while i < len(files) - 1:
        current_file = directory + files[i]
        next_file = directory + files[i + 1]

        
        
        if files_have_same_data(current_file, next_file):
            # Keep the earlier file, remove the later one
            #os.remove(next_file)
            print(f"Removing {next_file} since it is the same as {current_file}")
            files.pop(i + 1)  # Remove the file from our list since we deleted it
        else:
            i += 1


if __name__ == "__main__":
    remove_down_files(sys.argv[1])
    remove_duplicate_files(sys.argv[1])
