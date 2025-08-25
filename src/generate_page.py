import os
from src.extract_title import extract_title
from src.markdown_blocks import markdown_to_html_node

def create_dir(path):
    os.makedirs(path, exist_ok=True)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown_content = f.read()
    
    with open(template_path, "r") as f:
        template_content = f.read()
    
    node = markdown_to_html_node(markdown=markdown_content)
    html = node.to_html()
    title = extract_title(markdown_content)
    
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html)
    
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template_content)