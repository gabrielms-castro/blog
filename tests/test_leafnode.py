import unittest

from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(
            "a",
            "Click me",
            {
                "href": "https://www.clicked.com",
                "class":"class-styles"
            }
        ).to_html()
        self.assertEqual(
            node,
            '<a href="https://www.clicked.com" class="class-styles">Click me</a>'
        )
    
    def test_values(self):
        node = LeafNode(
            "p",
            "Some paragraph text"
        ).to_html()
        self.assertEqual(
            node,
            '<p>Some paragraph text</p>'
        )