import unittest

from src.htmlnode import HTMLNode
from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_a(self):
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
    
    def test_to_html_p(self):
        node = LeafNode(
            "p",
            "Some paragraph text"
        ).to_html()
        self.assertEqual(
            node,
            '<p>Some paragraph text</p>'
        )
    
    def test_to_html_no_tag(self):
        node = LeafNode(
            None,
            "Some paragraph text here without tag"
        ).to_html()
        self.assertEqual(
            node,
            "Some paragraph text here without tag"
        )
    

if __name__ == "__main__":
    unittest.main()