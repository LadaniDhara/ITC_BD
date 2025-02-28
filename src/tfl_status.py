import requests
import os
import json
from datetime import datetime

# TfL API URL for London Underground status
TFL_URL = "https://api.tfl.gov.uk/line/mode/tube/status"

def get_tube_status(app_id, app_key):
    """Fetches the London Underground status from TfL API."""
    params = {"app_id": app_id, "app_key": app_key}
    
    try:
        response = requests.get(TFL_URL, params=params)
        response.raise_for_status()  # Raise an error for HTTP issues
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_data_locally(data, filename="tfl_data.json"):
    """Saves API response as a JSON file."""
    if data:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved locally as {filename}")
    else:
        print("No data to save.")
