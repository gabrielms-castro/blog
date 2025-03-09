import unittest

from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )
                
    def test_values(self):
        node = HTMLNode(
            "div",
            "Some text",
        )
        # testing tag
        self.assertEqual(
            node.tag,
            "div"
        )
        
        # testing value
        self.assertEqual(
            node.value,
            "Some text"
        )
        
        # testing children
        self.assertEqual(
            node.children,
            None
        )
        
        # testing props == None
        self.assertEqual(
            node.props,
            None
        )
    
    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag: p, value: What a strange world, children: None, props: {'class': 'primary'})",
        )



if __name__ == "__main__":
    unittest.main()