import sqlite3
import json
import uuid
import os
import datetime


def get_date(file_name: str) -> str:
    """Time is in the format of YYYY-MM-DD"""
    return ("-".join(file_name.split("_")[1].split("-")[0:3])).split(".")[0]


def get_date_and_time(file_name: str) -> str:
    """Time is in the format of YYYY-MM-DD-HH-MM-SS"""
    return ("-".join(file_name.split("_")[1].split("-")[0:6])).split(".")[0]


def get_scheduled_departure_time(cursor, route, date, departure_time) -> str:
    # TODO: Check if this works.
    response = cursor.execute(
        f'SELECT "Scheduled Departure Time" FROM "Main Table" WHERE "Route Code"="{route["routeCode"]}" AND "Ferry Run Date"="{date}" ORDER BY ABS("Scheduled Departure Time" - "{departure_time}") LIMIT 1'
    ).fetchone()
    if response is None:
        return None
    return response[0]


def add_to_main_if_not_exist(cursor, route, sailing, date, scheduledDepartureTime) -> None:
    # Check if the status is future because if it is not then the time is actually the actual departure time and not the scheduled departure time
    # TODO: Check if this works
    if sailing["sailingStatus"] != "future":
        return None

    response = cursor.execute(
        f'SELECT * FROM "Main Table" WHERE "Route Code"="{route["routeCode"]}" AND "Ferry Run Date"="{date}" AND "Scheduled Departure Time"="{scheduledDepartureTime}"'
    ).fetchone()
    if response is None:
        cursor.execute(
            f'INSERT INTO "Main Table" ("Route Code", "Ferry Run Date", "Scheduled Departure Time", "From Terminal", "To Terminal", "Vessel Name", "Sailing Duration") VALUES ("{route["routeCode"]}", "{date}", "{scheduledDepartureTime}", "{route["fromTerminalCode"]}", "{route["toTerminalCode"]}", "{sailing["vesselName"]}", "{route["sailingDuration"]}");'
        )


DIRECTORY = "BC_Ferries_API_DATA"


connection = sqlite3.connect("database.db")
with open("db_init.sql") as f:
    script = f.read()
cursor = connection.executescript(script)


total_entries = 0
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
    DateAndTime = get_date_and_time(file)

    SeenAlready = {}
    for route in data:
        for sailing in route["sailings"]:
            sailing["time"] = datetime.datetime.strptime(sailing["time"], "%I:%M %p").strftime("%H:%M")
            sailing["arrivalTime"] = (
                datetime.datetime.strptime(sailing["arrivalTime"], "%I:%M %p").strftime("%H:%M")
                if sailing["arrivalTime"] != ""
                else ""
            )




            scheduled_departure_time = get_scheduled_departure_time(cursor, route, Date, sailing["time"])


            Date = (datetime.datetime.strptime(Date, "%Y-%m-%d") + datetime.timedelta(days=DateDifference)).strftime(
                "%Y-%m-%d"
            )


            # Add to the main table if it does not exist
            add_to_main_if_not_exist(cursor, route, sailing, Date, scheduled_departure_time)

            # TODO: CHange the entry for scheduled departure time to be the actual departure time
            Command = f"""INSERT INTO "Route Data" 
(
	"Route Code",
    "Scheduled Departure Time",
	"Ferry Run Date",
	"Sample Time",
	"Departure Time",
	"Arrival Time",
	"Sailing Status",
	"Total Fill",
	"All Size Fill",
	"7ft Under Fill"
) VALUES
("{route["routeCode"]}", 
"{scheduled_departure_time}", 
"{Date}", 
"{DateAndTime}", 
"{sailing["time"]}", 
"{sailing["arrivalTime"]}", 
"{sailing["sailingStatus"]}", 
"{sailing["fill"]}", 
"{sailing["carFill"]}", 
"{sailing["oversizeFill"]}");"""
            # print(Command)
            cursor.execute(Command)

            


            total_entries += 1
            if total_entries % 10000 == 0:
                print(total_entries)

connection.commit()
connection.close()
