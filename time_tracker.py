import csv
import json
import pandas as pd
from time import sleep
from datetime import datetime
from psutil import process_iter
from os.path import dirname, abspath, join, exists

TIME_INTERVAL_IN_SECONDS = 5
REPORT_CSV = join(dirname(abspath(__file__)), "report.csv")
REPORT_JSON = join(dirname(abspath(__file__)), "daily.json")
TARGET_PROCESSES = [
    {"exe": "TslGame.exe", "name": "PUBG"},
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


def update_json_stats(seconds: int = 0):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    with open(REPORT_JSON, "w", encoding="utf-8") as file:
        data = {today(): {"hour(s)": hours, "minute(s)": minutes, "second(s)": seconds}}
        json.dump(data, file, indent=4)


def update_csv_stats(hours, minutes):
    if not exists(REPORT_CSV):
        rows = [
            ["date", "hours", "minutes"],
            [today(), hours, minutes],
        ]
    else:
        with open(REPORT_CSV, mode="r", newline="") as file:
            rows = []
            for row in csv.reader(file):
                if row[0] == today():
                    rows.append([today(), hours, minutes])
                else:
                    rows.append(row)

        data = pd.read_csv(REPORT_CSV)
        if today() not in data.iloc[:, 0].values:
            rows.append([today(), hours, minutes])

    with open(REPORT_CSV, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def write_summary():
    if exists(REPORT_JSON):
        with open(REPORT_JSON, "r") as file:
            data = json.load(file)
            if not today() in data:
                update_json_stats()
            else:
                time_counter = data[today()]
                seconds = (
                    time_counter["hour(s)"] * 3600
                    + time_counter["minute(s)"] * 60
                    + time_counter["second(s)"]
                )
                update_json_stats(seconds + TIME_INTERVAL_IN_SECONDS)
                update_csv_stats(time_counter["hour(s)"], time_counter["minute(s)"])
    else:
        update_json_stats()


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
