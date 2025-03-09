

from src.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self,tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)
        if self.children is not None:
            raise ValueError("LeafNode cannot have children attribute")
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes must have a value")
        
        if self.tag is None:
            return str(self.value)
        
        props_html = self.props_to_html()
        
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"