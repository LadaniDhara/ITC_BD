import requests
import csv
from datetime import datetime
import re
import os

# API URLs
URL_STATUS = "https://api.tfl.gov.uk/Line/Mode/tube/Status"

# HDFS Directory Path
HDFS_DIRECTORY = "/tmp/big_datajan2025/TFL/TFLUndertube"

# Get current timestamp for file naming
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
csv_filename = f"underground_{timestamp}.csv"
local_csv_path = f"/tmp/{csv_filename}"  
hdfs_file_path = f"{HDFS_DIRECTORY}/{csv_filename}"

# Function to get stations for a given line
def get_line_route(line_id):
    url_route = f"https://api.tfl.gov.uk/Line/{line_id}/StopPoints"
    response_route = requests.get(url_route)
    data_route = response_route.json()
    return [stop["commonName"] for stop in data_route]

# Prepare data rows
rows = []

# Regex pattern to extract delay time
DELAY_PATTERN = r"(\d+)\s?minute[s]?\s?delay"

# Fetch TfL Underground status data
response_status = requests.get(URL_STATUS)
data_status = response_status.json()

# Initialize record ID counter
record_id = 1

for line in data_status:
    line_name = line["name"]
    line_id = line["id"]
    stations = get_line_route(line_id)
    stations_str = ", ".join(stations).replace('"', '').strip()  # Remove unwanted quotes

    for status in line["lineStatuses"]:
        status_description = status["statusSeverityDescription"]
        reason = status.get("reason", "No Delay")

        # Extract delay time if present
        delay_time = "N/A"
        match = re.search(DELAY_PATTERN, reason, re.IGNORECASE)
        if match:
            delay_time = match.group(1)

        # Append row to CSV data
        rows.append([
            record_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            line_name,
            status_description,
            reason,
            delay_time,
            stations_str
        ])

        record_id += 1

# Check if local file exists
file_exists = os.path.exists(local_csv_path)

# Write data to local CSV
with open(local_csv_path, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Write headers only if the file does not exist
    if not file_exists:
        writer.writerow(["Record_ID", "Timedetails", "Line", "Status", "Reasons", "Delay Time (Minutes)", "Route (Stations)"])

    # Append rows without headers if the file already exists
    writer.writerows(rows)

print(f"Data saved locally: {local_csv_path}")

# Ensure HDFS directory exists
os.system(f"hdfs dfs -mkdir -p {HDFS_DIRECTORY}")

# Upload to HDFS
os.system(f"hdfs dfs -put {local_csv_path} {hdfs_file_path}")

print(f"Data stored in HDFS: {hdfs_file_path}")
