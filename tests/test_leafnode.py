import unittest

from src.htmlnode import LeafNode, ParentNode


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
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )        
        
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
        
    

if __name__ == "__main__":
    unittest.main()