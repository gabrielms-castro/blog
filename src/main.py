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
    
    generate_page(
        from_path="content/blog/glorfindel/index.md",
        template_path="./template.html",
        dest_path="public/blog/glorfindel.html"
    )
    
    generate_page(
        from_path="content/blog/majesty/index.md",
        template_path="./template.html",
        dest_path="public/blog/majesty.html"
    )
    
    generate_page(
        from_path="content/blog/tom/index.md",
        template_path="./template.html",
        dest_path="public/blog/tom.html"
    )
    
    generate_page(
        from_path="content/contact/index.md",
        template_path="./template.html",
        dest_path="public/contact.html"
    )
    
if __name__ == "__main__":
    main()