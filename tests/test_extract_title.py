import unittest

from src.extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
# Sample Title
## Subtitle
Some content here.
"""
        title = extract_title(markdown)
        self.assertEqual(title, "Sample Title")
    
    def test_no_title(self):
        markdown = ""
        title = extract_title(markdown)
        self.assertIsNone(title)
    
    def test_only_subtitle(self):
        markdown = "## Subtitle"
        title = extract_title(markdown)
        self.assertIsNone(title)

if __name__ == "__main__":
    unittest.main()        