import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        print(node1)
        print(node2)
        self.assertEqual(node1, node2)
    
    def test_not_eq(self):
        node3 = TextNode("This is a link node", TextType.LINK)
        node4 = TextNode("This is a code node", TextType.CODE)
        print(node3)
        print(node4)
        self.assertNotEqual(node3, node4)
    
    def test_url_none(self):
        node5 = TextNode("This is a link node", TextType.LINK)
        print(node5)
        self.assertIsNone(node5.url)
        
    def test_url_not_none(self):
        node6 = TextNode("This is a link node", TextType.LINK, url="www.test.com")
        print(node6)
        self.assertIsNotNone(node6.url)
    
if __name__ == "__main__":
    unittest.main()