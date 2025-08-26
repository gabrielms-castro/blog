import os
from src.config import BASE_DIR
from src.extract_title import extract_title
from src.markdown_blocks import markdown_to_html_node

def create_dir(path):
    os.makedirs(path, exist_ok=True)

def generate_page(from_path, template_path, dest_path, basepath):
    
    with open(from_path, "r") as f:
        markdown_content = f.read()
    
    with open(template_path, "r") as f:
        template_content = f.read()
    
    node = markdown_to_html_node(markdown=markdown_content)
    html = node.to_html()
    title = extract_title(markdown_content)
    
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html)
    
    basepath = basepath if basepath.endswith("/") else basepath + "/"
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')
        
    create_dir(os.path.dirname(dest_path))
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_entries = os.listdir(dir_path_content)
    
    for entry in dir_entries:
        actual_dir_path_content = os.path.join(BASE_DIR, f"{dir_path_content}/{entry}")
        
        if os.path.isfile(actual_dir_path_content) and entry.endswith(".md"):
            dest_dir_ = actual_dir_path_content.replace(".md", ".html").replace(dir_path_content, dest_dir_path)

            generate_page(
                from_path=actual_dir_path_content,
                template_path=template_path,
                dest_path=dest_dir_,
                basepath=basepath
            )
        
        if os.path.isdir(actual_dir_path_content):
            generate_pages_recursive(
                dir_path_content=actual_dir_path_content,
                template_path=template_path,
                dest_dir_path=os.path.join(dest_dir_path, entry),
                basepath=basepath
            )

    