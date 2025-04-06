from enum import Enum
import re

from src.htmlnode import ParentNode
from src.inline_markdown import text_to_textnodes
from src.textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

    
def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    
    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        return BlockType.QUOTE
    
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)
        
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block):
    
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    
    raise ValueError(f"Unknown block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)    
    
def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") and not block.endswith("```"):
        raise ValueError("Code block must start and end with ```")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.CODE)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])
    
def quote_to_html_node(block):
    ...

def unordered_list_to_html_node(block):
    ...

def ordered_list_to_html_node(block):
    ...