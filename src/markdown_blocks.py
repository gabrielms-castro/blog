from enum import Enum
import html
import re
import textwrap

from src.htmlnode import LeafNode, ParentNode
from src.inline_markdown import text_to_textnodes, split_nodes_image, split_nodes_link
from src.textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    HR = "hr"
    TABLE = "table"
    HTML = "html"

HR_PATTERN = re.compile(r"^(-{3,}|\*{3,}|_{3,})$")
HTML_PATTERN = re.compile(r"^<([a-zA-Z/]|!--)")
TABLE_SEPARATOR_PATTERN = re.compile(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?$")
ORDERED_ITEM_PATTERN = re.compile(r"^(\d+)\. ")

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    current_lines = []
    in_fence = False

    def flush():
        block = textwrap.dedent("\n".join(current_lines)).strip()
        if block:
            blocks.append(block)
        current_lines.clear()

    for line in markdown.split("\n"):
        if line.lstrip().startswith("```"):
            if not in_fence:
                # a fence always starts a new block
                flush()
                in_fence = True
                current_lines.append(line)
            else:
                # a closing fence always ends the block
                current_lines.append(line)
                in_fence = False
                flush()
            continue

        if line.strip() == "" and not in_fence:
            flush()
        else:
            current_lines.append(line)

    flush()
    return blocks


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    code_lines = textwrap.dedent(block).split("\n")
    if len(code_lines) > 1 and code_lines[0].startswith("```") and code_lines[-1].endswith("```"):
        return BlockType.CODE

    if HR_PATTERN.match(block):
        return BlockType.HR

    if HTML_PATTERN.match(block):
        return BlockType.HTML

    if (
        len(lines) > 1
        and all(line.strip().startswith("|") for line in lines)
        and TABLE_SEPARATOR_PATTERN.match(lines[1].strip())
    ):
        return BlockType.TABLE

    if block.startswith(">"):
        return BlockType.QUOTE

    if block.startswith("- ") or block.startswith("* "):
        for line in lines:
            if not line.startswith("- ") and not line.startswith("* "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    first = ORDERED_ITEM_PATTERN.match(block)
    if first:
        i = int(first.group(1))
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
        case BlockType.HR:
            return LeafNode("hr", "")
        case BlockType.TABLE:
            return table_to_html_node(block)
        case BlockType.HTML:
            return html_block_to_html_node(block)
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

def slugify(text):
    """GitHub-style heading anchor: '4. Deploy da aplicação' -> '4-deploy-da-aplicação'."""
    text = re.sub(r"!?\[([^\[\]]*)\]\([^\(\)]*\)", r"\1", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")

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
    return ParentNode(f"h{level}", children, {"id": slugify(text)})

def code_to_html_node(block):
    block = textwrap.dedent(block)
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Code block must start and end with ```")
    first_line, _, rest = block.partition("\n")
    language = first_line[3:].strip()
    text = rest[:-3]
    code = LeafNode("code", html.escape(text, quote=False), {"class": f"language-{language}"} if language else None)
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
        text = ORDERED_ITEM_PATTERN.sub("", item, count=1)
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    start = int(ORDERED_ITEM_PATTERN.match(block).group(1))
    return ParentNode("ol", html_items, {"start": start} if start != 1 else None)

def _table_cells(row):
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [cell.strip() for cell in row.split("|")]

def _table_alignments(separator):
    alignments = []
    for cell in _table_cells(separator):
        if cell.startswith(":") and cell.endswith(":"):
            alignments.append("center")
        elif cell.endswith(":"):
            alignments.append("right")
        elif cell.startswith(":"):
            alignments.append("left")
        else:
            alignments.append(None)
    return alignments

def table_to_html_node(block):
    lines = block.split("\n")
    alignments = _table_alignments(lines[1])

    def row_to_html_node(row, cell_tag):
        cells = []
        for i, cell in enumerate(_table_cells(row)):
            align = alignments[i] if i < len(alignments) else None
            props = {"style": f"text-align: {align}"} if align else None
            cells.append(ParentNode(cell_tag, text_to_children(cell), props))
        return ParentNode("tr", cells)

    thead = ParentNode("thead", [row_to_html_node(lines[0], "th")])
    body_rows = [row_to_html_node(row, "td") for row in lines[2:]]
    children = [thead]
    if body_rows:
        children.append(ParentNode("tbody", body_rows))
    return ParentNode("div", [ParentNode("table", children)], {"class": "table-wrapper"})

def html_block_to_html_node(block):
    # raw HTML is passed through untouched; standalone comments are dropped
    if re.fullmatch(r"<!--.*?-->", block, re.DOTALL):
        return LeafNode(None, "")
    return LeafNode(None, block)
