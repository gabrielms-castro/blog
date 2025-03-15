import unittest

from src.extractor import extract_markdown_images, extract_markdown_links

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_image_1(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            matches,
            [
                ('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), 
                ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')
            ],
        )
        
    def test_extract_image_2(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            matches,
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png")
            ],
        )
    
    def test_extract_link(self):
        text = "Check this out: [some link](https://example.com) and ![an image](https://example.com/image.png)."
        matches = extract_markdown_links(text)
        self.assertListEqual(
            matches,
             [
                 ('some link', 'https://example.com')
            ]
        )
        
