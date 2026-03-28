import json
import sys

from src.config import BASE_DIR
from src.copy_files import static_to_public
from src.generate_page import generate_page, generate_pages_recursive
from src.textnode import TextNode, TextType

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print("Copying static files...")
    static_to_public(dest="docs", src="static")

    print("Generating pages...")
    posts = generate_pages_recursive(
        dir_path_content="content",
        template_path="./template.html",
        dest_dir_path="docs",
        basepath=basepath
    )

    print("Writing search index...")
    index_path = BASE_DIR / 'docs' / 'search-index.json'
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
