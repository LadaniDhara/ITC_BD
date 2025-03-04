import requests
import csv
import sys
from datetime import datetime
import re

# API Call for Line Status
url_status = "https://api.tfl.gov.uk/Line/Mode/tube/Status"
response_status = requests.get(url_status)
data_status = response_status.json()

# Function to get the stations for a given line
def get_line_route(line_id):
    url_route = f"https://api.tfl.gov.uk/Line/{line_id}/StopPoints"
    response_route = requests.get(url_route)
    data_route = response_route.json()
    
    stations = [stop["commonName"] for stop in data_route]
    return stations

# Prepare data rows
rows = []
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Regex pattern to extract delay time (in minutes)
delay_pattern = r"(\d+)\s?minute[s]?\s?delay"

for line in data_status:
    line_name = line["name"]
    line_id = line["id"]
    
    stations = get_line_route(line_id)
    stations_str = ", ".join(stations)
    
    for status in line["lineStatuses"]:
        status_description = status["statusSeverityDescription"]
        reason = status.get("reason", "No Delay")
        
        delay_time = "N/A"
        match = re.search(delay_pattern, reason, re.IGNORECASE)
        if match:
            delay_time = match.group(1)
        
        rows.append([timestamp, line_name, status_description, reason, delay_time, stations_str])

# Output CSV content to stdout
csv_writer = csv.writer(sys.stdout)
csv_writer.writerow(["Timestamp", "Line", "Status", "Reason", "Delay Time (Minutes)", "Route (Stations)"])
csv_writer.writerows(rows)
