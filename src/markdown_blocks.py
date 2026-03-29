from enum import Enum
import re

from src.htmlnode import ParentNode
from src.inline_markdown import text_to_textnodes, split_nodes_image, split_nodes_link
from src.textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    current_lines = []
    in_fence = False

    for line in markdown.split("\n"):
        if line.startswith("```"):
            in_fence = not in_fence

        if line == "" and not in_fence:
            block = "\n".join(current_lines).strip()
            if block:
                blocks.append(block)
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        block = "\n".join(current_lines).strip()
        if block:
            blocks.append(block)

    return blocks

    
def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    
    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        return BlockType.QUOTE
    
    if block.startswith("- ") or block.startswith("* "):
        for line in lines:
            if not line.startswith("- ") and not line.startswith("* "):
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
        try:
            html_node = block_to_html_node(block)
        except Exception as e:
            preview = block[:120].replace("\n", "\\n")
            raise ValueError(f"Error parsing block: '{preview}'\n  Caused by: {e}") from e
        children.append(html_node)
    return ParentNode("div", children)
        
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case _:
            raise ValueError(f"Unknown block type")
    
def _inline_links(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return [text_node_to_html_node(n) for n in nodes]

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        if text_node.text_type == TextType.BOLD:
            children.append(ParentNode("b", _inline_links(text_node.text)))
        elif text_node.text_type == TextType.ITALIC:
            children.append(ParentNode("i", _inline_links(text_node.text)))
        else:
            children.append(text_node_to_html_node(text_node))
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
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Code block must start and end with ```")
    text = block[block.index("\n")+1:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])
        
def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[1:].lstrip()
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def ordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)
    