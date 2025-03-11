class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag              # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value          # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children    # A list of HTMLNode objects representing the children of this node
        self.props = props          # A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
    
    def to_html(self):
        raise NotImplementedError # child classes will override this

    def props_to_html(self):
        if self.props is None:
            return ""
        
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
    
    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props=props)
        
        if self.value is not None:
            raise AttributeError("ParentNode does not have value attribute")
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode without 'tag' attribute")
        
        if self.children is None:
            raise ValueError("ParentNode without 'children' attribute")
        
        html_string = f"<{self.tag}>"
        
        for child in self.children:
            html_string += child.to_html()
            
        html_string += f"</{self.tag}>"
        
        return html_string

class LeafNode(HTMLNode):
    def __init__(self,tag, value, props=None):
        super().__init__(tag, value, None, props=props)
        
        if self.children is not None:
            raise AttributeError("LeafNode cannot have children attribute")
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf nodes must have a value")
        
        if self.tag is None:
            return str(self.value)
        
        props_html = self.props_to_html()
        
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"