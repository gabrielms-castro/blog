from src.copy_files import static_to_public
from src.textnode import TextNode, TextType

def main():
    static_to_public()
    text_node = TextNode(text="some text", text_type=TextType.TEXT, url="www.blablabla.com")
    print(text_node)
    
if __name__ == "__main__":
    main()