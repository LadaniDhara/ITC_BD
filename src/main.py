import os
from dotenv import load_dotenv
from src.tfl_status import get_tube_status
from src.utils import format_tube_status

# Load environment variables
load_dotenv()

# TfL API credentials
APP_ID = os.getenv("TFL_APP_ID")
APP_KEY = os.getenv("TFL_APP_KEY")

if not APP_ID or not APP_KEY:
    print("Error: Missing TfL API credentials. Check your .env file.")
    exit(1)

def main():
    """Main function to fetch and display Tube status."""
    data = get_tube_status(APP_ID, APP_KEY)
    print(format_tube_status(data))

if __name__ == "__main__":
    main()
