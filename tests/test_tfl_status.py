import unittest
from src.tfl_status import get_tube_status
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TestTFLStatus(unittest.TestCase):

    def test_get_tube_status(self):
        """Test if the API returns a valid response."""
        app_id = os.getenv("TFL_APP_ID")
        app_key = os.getenv("TFL_APP_KEY")

        self.assertIsNotNone(app_id, "TFL_APP_ID is missing")
        self.assertIsNotNone(app_key, "TFL_APP_KEY is missing")

        data = get_tube_status(app_id, app_key)
        self.assertIsInstance(data, list, "Response should be a list")
        self.assertGreater(len(data), 0, "Response should not be empty")

if __name__ == "__main__":
    unittest.main()
