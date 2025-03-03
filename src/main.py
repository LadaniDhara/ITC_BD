import os
from dotenv import load_dotenv
from src.tfl_status import get_tube_status, save_data_locally
from src.hdfs_uploader import upload_to_hdfs

# Load environment variables
load_dotenv()

# TfL API credentials
APP_ID = os.getenv("TFL_APP_ID")
APP_KEY = os.getenv("TFL_APP_KEY")

if not APP_ID or not APP_KEY:
    print("Error: Missing TfL API credentials. Check your .env file.")
    exit(1)

def main():
    """Fetch TfL data, save locally, and upload to HDFS."""
    data = get_tube_status(APP_ID, APP_KEY)
    filename = "tfl_data.json"
    save_data_locally(data, filename)

    # Define HDFS path
    hdfs_path = "/data/tfl/raw/tfl_data.json"
    upload_to_hdfs(filename, hdfs_path)

if __name__ == "__main__":
    main()
