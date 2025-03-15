import re

def extract_markdown_images(text):
    """takes raw markdown text and returns a list of tuples

    Args:
        text (string): raw markdown text
    """
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    return matches
    
    
def extract_markdown_links(text):
    """extracts markdown links instead of images

    Args:
        text (string): raw markdown text
    """
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)",text)
    return matches
