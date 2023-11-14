# tests/data_reading.py

import unittest
import sys
import os

# Add the path to the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import functions from content_extractor.py
from content_extractor import ContentExtractor

class TestDataReading(unittest.TestCase):
    def setUp(self):
        self.content_extractor = ContentExtractor()

    def tearDown(self):
        # Clean up any created files after each test
        for file_name in ['test_data_utf8.csv', 'test_data_cp1252.csv', 'test_data_missing_column.csv', 'test_data_empty_file.csv']:
            if os.path.exists(file_name):
                os.remove(file_name)

    def test_read_data_cp1252(self):
        # Test reading data with CP1252 encoding
        file_name = "test_data_cp1252.csv"
        data = "LinkURI|Description\nhttps://example.com|Sample data"
        with open(file_name, "w", encoding="cp1252") as file:
            file.write(data)

        # Ensure the method doesn't raise an exception
        df = self.content_extractor.read_data(file_name)

        # Assertions based on the test data
        self.assertTrue("URL" in df.columns)
        self.assertEqual(df.shape, (1, 2))
        self.assertEqual(df.iloc[0]["URL"], "https://example.com")
        self.assertEqual(df.iloc[0]["Description"], "Sample data")

    def test_read_data_missing_column(self):
        # Test handling missing URL column
        file_name = "test_data_missing_column.csv"
        data = "InvalidColumnName|Description\nhttps://example.com|Sample data"
        with open(file_name, "w", encoding="cp1252") as file:
            file.write(data)

        # Ensure the method raises a ValueError with the expected message
        with self.assertRaises(ValueError) as context:
            self.content_extractor.read_data(file_name)
        self.assertIn("Column 'LinkURI' not found", str(context.exception))

    def test_read_data_empty_file(self):
        # Test handling empty CSV file
        file_name = "test_data_empty_file.csv"
        with open(file_name, "w", encoding="cp1252") as file:
            file.write("")

        # Ensure the method raises a ValueError with the expected message
        with self.assertRaises(ValueError) as context:
            self.content_extractor.read_data(file_name)
        self.assertIn("The CSV file is empty", str(context.exception))

if __name__ == "__main__":
    unittest.main()
