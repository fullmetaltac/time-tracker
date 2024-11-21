import json
from time import sleep
from datetime import datetime
from psutil import process_iter
from os.path import dirname, abspath, join, exists

#################################################
#   This is a simple time tracker to monitor    #
#   how much time I spend playing video games   #
#   during the day.                             #
#                                               #
#   Setup:                                      #
#   1. set REPORT_FILE variable                 #
#   2. set TARGET_PROCESSES variable            #
#   3. set TIME_INTERVAL_IN_SECONDS variable    #
#   4. pip install psutil                       #
#   5. python time_tracker.py                   #
#################################################

TIME_INTERVAL_IN_SECONDS = 5
REPORT_FILE = join(dirname(abspath(__file__)), "time_report.json")
TARGET_PROCESSES = [
    {"exe": "TslGame.exe", "name": "PUBG"},
    {"exe": "Telegram.exe", "name": "Telegram"},
    {"exe": "SC2_x64.exe", "name": "StarCraft II"},
    {"exe": "RainbowSix.exe", "name": "Rainbow Six Siege"},
    {"exe": "SHProto-Win64-Shipping.exe", "name": "Silent Hill 2"},
]


def today():
    return datetime.now().strftime("%Y-%m-%d")


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_message(process):
    elapsed_time = datetime.now() - datetime.fromtimestamp(process._create_time)
    hours = int(elapsed_time.seconds // 3600)
    minutes = int((elapsed_time.seconds % 3600) // 60)
    seconds = int(elapsed_time.seconds % 60)

    names = [x["name"] for x in TARGET_PROCESSES]
    name = [x for x in TARGET_PROCESSES if x["exe"] == process.info["name"]][0]["name"]
    name = name.ljust(len(max(names, key=len)), ".")

    print(f"{now()} [ {name} ] {hours:02d}:{minutes:02d}:{seconds:02d} ")


def write_to_file(seconds: int = 0):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        data = {today(): {"hour(s)": hours, "minute(s)": minutes, "second(s)": seconds}}
        json.dump(data, file, indent=4)


def write_summary():
    if exists(REPORT_FILE):
        with open(REPORT_FILE, "r") as file:
            data = json.load(file)
            if not today() in data:
                write_to_file()
            else:
                time_counter = data[today()]
                seconds = (
                    time_counter["hour(s)"] * 3600
                    + time_counter["minute(s)"] * 60
                    + time_counter["second(s)"]
                )
                write_to_file(seconds + TIME_INTERVAL_IN_SECONDS)
    else:
        write_to_file()


def active_processes(targets):
    exes = [t["exe"] for t in targets]
    results = []
    for process in process_iter(attrs=["name"]):
        if any([x.info["name"] == process.info["name"] for x in results]):
            continue
        if process.info["name"] in exes:
            results.append(process)
    return results


if __name__ == "__main__":
    while True:
        processes = active_processes(TARGET_PROCESSES)
        for process in processes:
            log_message(process)
        if len(processes):
            write_summary()
        sleep(TIME_INTERVAL_IN_SECONDS)
