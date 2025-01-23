import sqlite3
import json
import uuid
import os
import datetime


def get_date(file_name: str) -> str:
    """Time is in the format of YYYY-MM-DD-HH-MM-SS"""
    return ("-".join(file_name.split("_")[1].split("-")[0:6])).split(".")[0]


DIRECTORY = "BC_Ferries_API_DATA"


connection = sqlite3.connect("database.db")
cursor = connection.cursor()

# Capacity table: PK: DATE/ROUTECODE/TIME
response = cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='capacity';")
if response.fetchone() is None:
    cursor.execute(
        f"""CREATE TABLE [capacity] (
    [RouteCode] TEXT NULL,
    [FromTerminal] TEXT NULL,
    [ToTerminal] TEXT NULL,
    [SailingDuration] TEXT NULL,
    [time] TEXT NULL,
    [arrivalTime] TEXT NULL,
    [SailingStatus] TEXT NULL,
    [Fill] TEXT NULL,
    [CarFill] TEXT NULL,
    [OverSizeFill] TEXT NULL,
    [VesselName] TEXT NULL,
    [VesselStatus] TEXT NULL,
    [yearAndDate] TEXT NULL);"""
    )

# Get data from json file
for file in os.listdir("BC_Ferries_API_DATA"):
    # Check if file is a capacity file
    if not file.startswith("capacity"):
        continue

    # Load data from json file
    with open(f"{DIRECTORY}/{file}") as f:
        data = json.load(f)

    # Check that the service was not down when it was queried
    if "routes" not in data:
        continue

    data = data["routes"]

    # Get the date of the file
    Date = get_date(file)

    for route in data:
        for sailing in route["sailings"]:
            cursor.execute(
                f"""INSERT INTO capacity (RouteCode, FromTerminal, ToTerminal, SailingDuration, time, arrivalTime, SailingStatus, Fill, CarFill, OverSizeFill, VesselName, VesselStatus, yearAndDate) 
                VALUES ("{route["routeCode"]}", "{route["fromTerminalCode"]}", "{route["toTerminalCode"]}", "{route["sailingDuration"]}", "{sailing["time"]}", "{sailing["arrivalTime"]}", "{sailing["sailingStatus"]}", "{sailing["fill"]}", "{sailing["carFill"]}", "{sailing["oversizeFill"]}", "{sailing["vesselName"]}", "{sailing["vesselStatus"]}", "{Date}");"""
            )

connection.commit()
connection.close()
