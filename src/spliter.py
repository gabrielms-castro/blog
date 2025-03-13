from src.textnode import TextNode, TextType


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
