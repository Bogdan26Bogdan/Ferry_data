import os
import sys
import datetime


def get_last_push_time():
    # Get the last push time
    # Pushed to git at $(TZ="America/Vancouver" date)"
    filecontents = ""
    for line in sys.stdin:
        filecontents += line

    lines = filecontents.split("\n")
    lines = [line for line in lines if "Pushed to git at" in line]
    times = [(line.split("Pushed to git at ")[1]).split(" PST")[0] for line in lines]
    actual_times = []
    for str_time in times:
        time = datetime.datetime.strptime(str_time, "%a %d %b %Y %I:%M:%S %p")
        actual_times.append(time.timestamp())

    print(str(max(actual_times)).split(".")[0])
    
if __name__ == "__main__":
    get_last_push_time()
