# # tests/chat_openai.py

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

    def test_extract_single_event_chatopenai(self):
        # Create a sample DataFrame with one event
        sample_data = {'URL': ['https://example.com'],
                       'New_Content': ['Sample content']}
        sample_df = pd.DataFrame(sample_data)

        # Call the extract_single_event_chatopenai function
        result_df = self.content_extractor.extract_single_event_chatopenai(
            url_content=sample_df['New_Content'].iloc[0],
            url=sample_df['URL'].iloc[0]
        )

        # Perform assertions based on expected results
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertTrue('is_happened' in result_df.columns)
        self.assertTrue('event_name_en' in result_df.columns)
        # Add more assertions based on the expected structure of the result DataFrame

    def test_extract_events_chatopenai(self):
        # Create a sample DataFrame with multiple events
        sample_data = {'URL': ['https://example.com', 'https://example.org'],
                       'New_Content': ['Sample content 1', 'Sample content 2']}
        sample_df = pd.DataFrame(sample_data)

        # Call the extract_events_chatopenai function
        result_df = self.content_extractor.extract_events_chatopenai(
            df=sample_df
        )

        # Perform assertions based on expected results
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertTrue('is_happened' in result_df.columns)
        self.assertTrue('event_name_en' in result_df.columns)
        # Add more assertions based on the expected structure of the result DataFrame

    def tearDown(self):
        # Clean up any resources after each test if needed
        pass

if __name__ == '__main__':
    unittest.main()
