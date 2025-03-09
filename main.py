from src.textnode import TextNode, TextType


def main():
    text_node = TextNode(text="some text", text_type=TextType.TEXT, url="ww.bblabla.com")
    print(text_node)
    
if __name__ == "__main__":
    main()