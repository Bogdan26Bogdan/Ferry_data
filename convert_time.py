import os
import datetime


OLD_Directory = "BC_Ferries_API_DATA/"
NEW_Directory = "BC_Ferries_API_DATA_NEW/"


def convert_time(utc_time: str) -> str:
    try:
        utc_time = datetime.datetime.strptime(utc_time, "%Y-%m-%d-%H-%M-%S")
        local_time = utc_time.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)  # None is localtime
        return local_time.strftime("%Y-%m-%d-%H-%M-%S")
    except(ValueError):
        return None      
    
def reconstruct_file_with_new_date(file_name:str, new_date:str) -> str:
    if new_date == None:
        return "None"
    return file_name.split("_")[0] + "_" + new_date + ".json"

for file in os.listdir(OLD_Directory):
    file_date = file.split("_")[-1].split(".")[0]

    #print(file_date, convert_time(file_date))
    #print(file, reconstruct_file_with_new_date(file, convert_time(file_date)))

    old_file = OLD_Directory + file
    new_file = NEW_Directory + reconstruct_file_with_new_date(file, convert_time(file_date))
    if "None" in new_file:
        print(f"Not moving: {old_file} as the converted is {new_file}")
        continue
    #print(f"Moving: {old_file} as the converted is {new_file}")
    os.rename(old_file, new_file)



        
