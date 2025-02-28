import requests
import csv
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
    
    # Extracting station names
    stations = [stop["commonName"] for stop in data_route]
    return stations

# CSV File Name
csv_file = "tfl_realtime_data_underground.csv"

# Prepare data rows
rows = []
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Regex pattern to extract delay time (in minutes) from reason description
delay_pattern = r"(\d+)\s?minute[s]?\s?delay"

for line in data_status:
    line_name = line["name"]
    line_id = line["id"]  # Get line ID for fetching its stations
    
    # Fetching the route (stations) for the current line
    stations = get_line_route(line_id)
    stations_str = ", ".join(stations)  # Joining station names into a single string
    
    for status in line["lineStatuses"]:
        status_description = status["statusSeverityDescription"]
        reason = status.get("reason", "No Delay")  # Get reason or default to "No delay"
        
        # Check if the reason includes a delay time (using regex)
        delay_time = "N/A"
        match = re.search(delay_pattern, reason, re.IGNORECASE)
        if match:
            delay_time = match.group(1)  # Extracted delay time in minutes
        
        # Adding the row with stations and delay information
        rows.append([timestamp, line_name, status_description, reason, delay_time, stations_str])

# Writing data to CSV
with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write header if the file is empty
    if file.tell() == 0:
        writer.writerow(["Timestamp", "Line", "Status", "Reason", "Delay Time (Minutes)", "Route (Stations)"])
    
    # Write data rows
    writer.writerows(rows)

print(f"Data saved to {csv_file}")
