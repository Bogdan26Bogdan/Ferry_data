import os
import sys
import datetime


def get_last_file_time(directory: str) -> datetime.datetime:
    files = os.listdir(directory)
    files = [file for file in files if "json" in file]
    times = [datetime.datetime.strptime(file.split("_")[1].split(".")[0], "%Y-%m-%d-%H-%M-%S") for file in files]
    return max(times)


def files_created_in_last_n_minutes(directory: str, n: int):
    last_file_time = get_last_file_time(directory)
    now = datetime.datetime.now()
    return (now - last_file_time).total_seconds() / 60 < n
    

if __name__ == "__main__":
    print(files_created_in_last_n_minutes(sys.argv[1], int(sys.argv[2])))