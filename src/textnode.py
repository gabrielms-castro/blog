from enum import Enum

from src.htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text            # text content of the node
        self.text_type = text_type  # type of text this node contains, which is a member of the TextType enum
        self.url = url              # URL of the link or image, if the text is a link. Default to None if nothing is passed in.
    
    def __eq__(self, other):
        return (
            self.text == other.text 
            and self.text_type == other.text_type
            and self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if TextType.TEXT == text_node.text_type:
        return LeafNode(None, text_node.text)
    
    if TextType.BOLD == text_node.text_type:
        return LeafNode("b", text_node.text)
    
    if TextType.ITALIC == text_node.text_type:
        return LeafNode("i", text_node.text)

    if TextType.CODE == text_node.text_type:
        return LeafNode("code", text_node.text)

    if TextType.LINK == text_node.text_type:
        return LeafNode("a", text_node.text, {"href":text_node.url})
    
    if TextType.IMAGE == text_node.text_type:
        return LeafNode("img", "", {"src": text_node.url, "alt":text_node.text})
    
    raise ValueError(f"{text_node.text_type} is not a valid text type")