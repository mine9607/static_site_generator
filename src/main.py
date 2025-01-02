from textnode import TextNode, TextType

def main():

    node = TextNode("This is a text node",TextType.BOLD_TEXT , "https://www.boot.dev")

    print(node)

if __name__ == "__main__":
    main()
