from src.copy_files import static_to_public
from src.generate_page import generate_page
from src.textnode import TextNode, TextType

def main():
    static_to_public()
    generate_page(
        from_path="content/index.md",
        template_path="./template.html",
        dest_path="public/index.html"
    )
    
if __name__ == "__main__":
    main()