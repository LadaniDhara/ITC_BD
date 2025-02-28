import requests
import os

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
