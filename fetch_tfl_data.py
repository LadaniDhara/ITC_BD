import requests
import csv
from datetime import datetime
import re
import os

# API Call for Line Status
URL_STATUS = "https://api.tfl.gov.uk/Line/Mode/tube/Status"

# Function to get stations for a given line
def get_line_route(line_id):
    url_route = f"https://api.tfl.gov.uk/Line/{line_id}/StopPoints"
    response_route = requests.get(url_route)
    data_route = response_route.json()
    
    # Extract station names
    return [stop["commonName"] for stop in data_route]

# CSV File Name (local)
LOCAL_CSV_FILE = "tfl_realtime_data_underground.csv"

# HDFS Target Path
HDFS_CSV_FILE = "/tmp/big_datajan2025/TFL/TFLUnderground/tfl_realtime_data_underground.csv"

# Prepare data rows
rows = []
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Regex pattern to extract delay time (in minutes) from reason description
DELAY_PATTERN = r"(\d+)\s?minute[s]?\s?delay"

# Fetch data
response_status = requests.get(URL_STATUS)
data_status = response_status.json()

for line in data_status:
    line_name = line["name"]
    line_id = line["id"]
    
    # Get stations for this line
    stations = get_line_route(line_id)
    stations_str = ", ".join(stations)  

    for status in line["lineStatuses"]:
        status_description = status["statusSeverityDescription"]
        reason = status.get("reason", "No Delay")

        # Extract delay time if available
        delay_time = "N/A"
        match = re.search(DELAY_PATTERN, reason, re.IGNORECASE)
        if match:
            delay_time = match.group(1)  

        # Append the row
        rows.append([timestamp, line_name, status_description, reason, delay_time, stations_str])

# Write data to CSV (Append mode)
write_header = not os.path.exists(LOCAL_CSV_FILE)

with open(LOCAL_CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    if write_header:
        writer.writerow(["Timestamp", "Line", "Status", "Reason", "Delay Time (Minutes)", "Route (Stations)"])
    writer.writerows(rows)

print(f"Data saved to {LOCAL_CSV_FILE}")

# Append CSV to HDFS
os.system(f"hdfs dfs -test -e {HDFS_CSV_FILE} || hdfs dfs -touchz {HDFS_CSV_FILE}")  # Ensure file exists
os.system(f"hdfs dfs -appendToFile {LOCAL_CSV_FILE} {HDFS_CSV_FILE}")

print(f"Data appended to HDFS: {HDFS_CSV_FILE}")
