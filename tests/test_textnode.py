import unittest

from src.textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_false(self):
        node = TextNode("This is a link node", TextType.LINK)
        node2 = TextNode("This is a link node", TextType.CODE)
        self.assertNotEqual(node, node2)
        
    def test_eq_false2(self):
        node = TextNode("This is a link node", TextType.LINK)
        node2 = TextNode("This is a link node2", TextType.LINK)
        self.assertNotEqual(node, node2)
        
    def test_eq_url(self):
        node = TextNode("This is a link node", TextType.LINK, "www.google.com")
        node2 = TextNode("This is a link node", TextType.LINK, "www.google.com")
        self.assertEqual(node, node2)
    
    def test_url_none(self):
        node = TextNode("This is a link node", TextType.LINK)
        self.assertIsNone(node.url)
        
    def test_url_not_none(self):
        node = TextNode("This is a link node", TextType.LINK, url="www.test.com")
        self.assertIsNotNone(node.url)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)",
            repr(node)
        )
    
if __name__ == "__main__":
    unittest.main()