# tests/data_cleaning.py

import unittest
import sys
import os

# Add the path to the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import functions from your_module
from content_extractor import ContentExtractor

class TestTextCleaning(unittest.TestCase):
    def setUp(self):
        self.content_extractor = ContentExtractor()
        
    def test_clean_text_html_tags(self):
        # Test cleaning HTML tags from text
        input_text = "<p>Hello, <b>world!</b></p>"
        expected_output = "Hello, world!"
        cleaned_text = self.content_extractor.clean_text(input_text)
        self.assertEqual(cleaned_text, expected_output)

    def test_clean_text_special_characters(self):
        # Test cleaning special characters from text
        input_text = "Hello, @world! How are you?"
        expected_output = "Hello, world! How are you"
        cleaned_text = self.content_extractor.clean_text(input_text)
        self.assertEqual(cleaned_text, expected_output)

    def test_clean_text_extra_whitespace(self):
        # Test removing extra whitespaces from text
        input_text = "   This    is   a   test.   "
        expected_output = "This is a test."
        cleaned_text = self.content_extractor.clean_text(input_text)
        self.assertEqual(cleaned_text, expected_output)


if __name__ == "__main__":
    unittest.main()
