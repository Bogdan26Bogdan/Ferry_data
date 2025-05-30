import requests
import json
import os
import sys
import time

# TODO: Replace with local server
end_points = [
    "http://localhost:8080/v2/capacity/",
    "http://localhost:8080/v2/noncapacity/",
    "http://localhost:8080/v2/",
]
date = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
DIRECTORY = "BC_Ferries_API_DATA/"


def get_name(name: str) -> str:
    name = name.split("/")
    for i in range(len(name) - 1, 0, -1):
        if name[i] != "":
            return name[i]


for end_point in end_points:
    response = requests.get(end_point)
    data = response.json()
    file_name = DIRECTORY + get_name(end_point) + "_" + date + ".json"
    with open(file_name, "w") as f:
        json.dump(data, f)
        print(f"{file_name} has been created")
