# # tests/url_content_extractor.py

import unittest
import sys
import os
import pandas as pd

# Add the path to the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import functions from your_module
from content_extractor import ContentExtractor

class TestContentExtractor(unittest.TestCase):
    def setUp(self):
        self.content_extractor = ContentExtractor()

    def test_extract_url_content_valid(self):
        # Provide a valid URL for testing
        valid_url = "https://example.com"
        summary, content, is_valid = self.content_extractor.extract_url_content(valid_url)

        # Perform assertions based on expected results
        self.assertIsInstance(summary, str)
        self.assertIsInstance(content, str)
        self.assertIsInstance(is_valid, int)
        self.assertTrue(is_valid in [0, 1])  # Ensure is_valid is either 0 or 1

    def test_extract_url_content_invalid(self):
        # Provide an invalid URL for testing
        invalid_url = "https://invalid-url"
        summary, content, is_valid = self.content_extractor.extract_url_content(invalid_url)

        # Perform assertions based on expected results
        self.assertEqual(summary, '')
        self.assertEqual(content, '')
        self.assertEqual(is_valid, 0)

    def test_extract_content(self):
        # Create a sample DataFrame for testing
        sample_data = {'URL': ['https://example1.com', 'https://example2.com'],
                       'Language': ['en', 'fr']}
        sample_df = pd.DataFrame(sample_data)

        # Test parallel content extraction
        extracted_df = self.content_extractor.extract_content(sample_df)

        # Perform assertions based on expected results
        self.assertTrue('Summary' in extracted_df.columns)
        self.assertTrue('New_Content' in extracted_df.columns)
        self.assertTrue('Is_Article' in extracted_df.columns)

        # Ensure the DataFrame shape is as expected
        self.assertEqual(extracted_df.shape, (2, 5))  # Assuming there are 5 columns in the result DataFrame

    def test_filter_scraped_data_valid(self):
        # Create a sample DataFrame with 'Is_Article' column
        sample_data = {'Summary': ['Summary 1', 'Summary 2'],
                       'New_Content': ['Content 1', 'Content 2'],
                       'Is_Article': [1, 0]}  # Example values, assuming 1 means valid article
        sample_df = pd.DataFrame(sample_data)

        # Call the filter_scraped_data function
        filtered_df = self.content_extractor.filter_scraped_data(sample_df)

        # Perform assertions based on expected results
        self.assertTrue('Summary' in filtered_df.columns)
        self.assertTrue('New_Content' in filtered_df.columns)
        self.assertTrue('Is_Article' in filtered_df.columns)
        self.assertEqual(filtered_df.shape[0], 1)  # Assuming only one valid article in the sample

    def test_filter_scraped_data_invalid_column(self):
        # Create a sample DataFrame without 'Is_Article' column
        sample_data = {'Summary': ['Summary 1', 'Summary 2'],
                       'New_Content': ['Content 1', 'Content 2']}
        sample_df = pd.DataFrame(sample_data)

        # Call the filter_scraped_data function
        filtered_df = self.content_extractor.filter_scraped_data(sample_df)

        # Perform assertions based on expected results
        self.assertEqual(filtered_df.shape[0], 0)  # Expecting an empty DataFrame


    def tearDown(self):
        # Clean up any resources after each test if needed
        pass

if __name__ == '__main__':
    unittest.main()
