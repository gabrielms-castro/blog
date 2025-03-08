from enum import Enum

class TextType(Enum):
    NORMAL = "normal text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "link"
    IMAGE = "image"
    
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text            # text content of the node
        self.text_type = text_type  # type of text this node contains, which is a member of the TextType enum
        self.url = url              # URL of the link or image, if the text is a link. Default to None if nothing is passed in.
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"