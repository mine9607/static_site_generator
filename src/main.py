from textnode import TextNode, TextType, text_to_text_nodes

def main():

    node = TextNode("This is a text node",TextType.BOLD, "https://www.boot.dev")

    print(node)

    # result1 = text_to_text_nodes("This is **bold** and *italic*")
    # result2 = text_to_text_nodes("Hello ![alt](url) and [link](url)")
    result3 = text_to_text_nodes("")

    # print(result1)
    # print(result2)
    print(result3)

if __name__ == "__main__":
    main()
