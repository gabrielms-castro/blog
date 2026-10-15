import unittest
from src.markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "#hashtag"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "---"
        self.assertEqual(block_to_block_type(block), BlockType.HR)
        block = "***"
        self.assertEqual(block_to_block_type(block), BlockType.HR)
        block = "| a | b |\n|---|---|\n| 1 | 2 |"
        self.assertEqual(block_to_block_type(block), BlockType.TABLE)
        block = "| a | b |\n| 1 | 2 |"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "<p>raw</p>"
        self.assertEqual(block_to_block_type(block), BlockType.HTML)
        block = "<!-- comment -->"
        self.assertEqual(block_to_block_type(block), BlockType.HTML)
        block = "<3 not html"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "3. list\n4. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "3. list\n5. items"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "   ```bash\n   code\n   ```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1 id=\"this-is-an-h1\">this is an h1</h1><p>this is paragraph text</p><h2 id=\"this-is-an-h2\">this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_horizontal_rule(self):
        md = "para one\n\n---\n\npara two\n\n***"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><p>para one</p><hr><p>para two</p><hr></div>")

    def test_heading_id_with_accents(self):
        md = "## 3. Configurar a integração entre as plataformas"
        html = markdown_to_html_node(md).to_html()
        self.assertIn('id="3-configurar-a-integração-entre-as-plataformas"', html)

    def test_table(self):
        md = """
| URL        | Directory |
|------------|:---------:|
| `/static/` | /home/x   |
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            '<div><div class="table-wrapper"><table>'
            '<thead><tr><th>URL</th><th style="text-align: center">Directory</th></tr></thead>'
            '<tbody><tr><td><code>/static/</code></td><td style="text-align: center">/home/x</td></tr></tbody>'
            "</table></div></div>",
        )

    def test_raw_html_and_comments(self):
        md = """
<!-- just a note -->

<p align="center"><img src="/a.png" alt="A" width="320"></p>
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, '<div><p align="center"><img src="/a.png" alt="A" width="320"></p></div>')

    def test_indented_fence_followed_by_image(self):
        md = """
2. Clone it:

   ```bash
   git clone repo
   ```
![shot](/shot.png)
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            '<div><ol start="2"><li>Clone it:</li></ol>'
            '<pre><code class="language-bash">git clone repo\n</code></pre>'
            '<p><img src="/shot.png" alt="shot"></p></div>',
        )

    def test_ordered_list_start(self):
        md = "3. three\n4. four"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, '<div><ol start="3"><li>three</li><li>four</li></ol></div>')

    def test_code_is_escaped(self):
        md = "```\n<div>&</div>\n```\n\nuse `<br>` here"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>&lt;div&gt;&amp;&lt;/div&gt;\n</code></pre>"
            "<p>use <code>&lt;br&gt;</code> here</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
