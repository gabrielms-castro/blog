from src.textnode import TextNode, TextType
from src.extractor import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    convert TextNodes to HTMLNodes. create TextNodes from raw markdown strings

    Args:
        old_nodes (list): list of nodes
        delimiter (string): delimiter to split old nodes
        text_type (TextType): TextType

    Returns:
        list: list of TextNode
    """
    
    if not old_nodes:
        return None
    
    new_nodes = []
    
    for old_node in old_nodes:
        
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        
        start_index = text.find(delimiter)
        if start_index == -1:
            new_nodes.append(old_node)
            continue
        
        end_index = text.find(delimiter, start_index + len(delimiter))
        if end_index == -1:
            raise ValueError(f"No closing delimiter {delimiter} found")
        
        before_text = text[:start_index]
        during_text = text[start_index + len(delimiter):end_index]
        after_text = text[end_index + len(delimiter):]
        
        if before_text:
            new_nodes.append(
                TextNode(before_text, TextType.TEXT)
            )
            
        new_nodes.append(
            TextNode(during_text, text_type)
        )
        
        if after_text:
            new_nodes.append(
                TextNode(after_text, TextType.TEXT)
            )
    
    return new_nodes


def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            remaining_text = node.text
            matches = extract_markdown_images(remaining_text)
            
            for alt_text, href in matches:
                image_text = f"![{alt_text}]({href})"
                
                if image_text in remaining_text:
                    before, remaining_text = remaining_text.split(image_text, 1)
                    
                    if before:
                        nodes.append(
                            TextNode(before, TextType.TEXT)
                        )
                    
                    nodes.append(
                        TextNode(alt_text, TextType.IMAGE, href)
                    )
                
            if remaining_text:
                nodes.append(
                    TextNode(remaining_text, TextType.TEXT)
                )
        else:
            nodes.append(node)
        
    return nodes

def split_nodes_link(old_nodes):
    nodes = []
    
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            remaining_text = node.text
            matches = extract_markdown_links(remaining_text)
            
            for title, href in matches:
                link_text = f"[{title}]({href})"
                
                if link_text in remaining_text:
                    before, remaining_text = remaining_text.split(link_text, 1)
                    
                    if before:
                        nodes.append(
                            TextNode(before, TextType.TEXT)
                        )
                    
                    nodes.append(
                        TextNode(title, TextType.LINK, href)
                    )
                
            if remaining_text:
                nodes.append(
                    TextNode(remaining_text, TextType.TEXT)
                )
        else:
            nodes.append(node)
        
    return nodes


node = TextNode(
    "This is text with an [link](https://www.facebook.com) and another [second link](http://www.google.com)",
    TextType.TEXT,
)
new_nodes = split_nodes_link([node])
print(new_nodes)


node = TextNode(
    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
    TextType.TEXT,
)
new_nodes = split_nodes_image([node])
print(new_nodes)