import sys

from src.copy_files import static_to_public
from src.generate_page import generate_page, generate_pages_recursive
from src.textnode import TextNode, TextType

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print("Copying static files...")
    static_to_public()
    
    print("Generating pages...")
    generate_pages_recursive(
        dir_path_content="content",
        template_path="./template.html",
        dest_dir_path="docs",
        basepath=basepath
    )
    
if __name__ == "__main__":
    main()