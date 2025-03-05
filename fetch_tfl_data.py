import requests
import csv
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Define API endpoints
endpoints = {
    "status": "https://api.tfl.gov.uk/Line/elizabeth/Status",
    "arrivals": "https://api.tfl.gov.uk/Line/elizabeth/Arrivals",
    "route": "https://api.tfl.gov.uk/Line/elizabeth/Route"
}

# Function to make API calls
def fetch_data(key, url):
    response = requests.get(url)
    return key, response.json() if response.status_code == 200 else f"Error: {response.status_code}"

# Use ThreadPoolExecutor for parallel requests
responses = {}
with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(lambda item: fetch_data(*item), endpoints.items())

# Store results
for key, data in results:
    responses[key] = data

# Generate a timestamped CSV filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"tfl_data_{timestamp}.csv"

# Save data to CSV
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write headers
    writer.writerow(["API Type", "Data"])

    # Write each API response into a new row
    for key, data in responses.items():
        writer.writerow([key, str(data)])  # Convert JSON to string for CSV storage

print(f"✅ Data saved to CSV: {csv_filename}")

# Define HDFS Path
HDFS_DIRECTORY = "/tmp/big_datajan2025/TFL/Elizabeth"
hdfs_file_path = f"{HDFS_DIRECTORY}/{csv_filename}"

# Ensure the HDFS directory exists
os.system(f"hdfs dfs -mkdir -p {HDFS_DIRECTORY}")

# Upload CSV file to HDFS
os.system(f"hdfs dfs -put -f {csv_filename} {hdfs_file_path}")

# Verify upload
os.system(f"hdfs dfs -ls {HDFS_DIRECTORY}")

print(f"✅ Data uploaded to HDFS: {hdfs_file_path}")
