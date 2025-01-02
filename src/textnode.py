from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class Delimiters(Enum):
    BOLD = "**"
    ITALIC = "*"
    CODE = "`"

delimiters ={
    "bold": "**",
    "italic": "*",
    "code":"`"
}

class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url # the URL of the link or image, if the text is a link

    def __eq__(self, other):
        # returns True if all properties of TextNode are equal to all properties of another
        return (
                self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url
                )

    def __repr__(self):
        # returns a string representation of the TextNode object
        text = f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        #print("Results of __repr__\n", text)
        return text


def text_node_to_html_node(text_node):
    # Normal Text should return a LeafNode with no tag just raw text value
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag ="", props = {}, value = text_node.text) #LeafNodes require tag, value, props

    # Bold Text should return a LeafNode with a "b" tag and the text
    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag ="b",  props = {}, value = text_node.text)

    # Italic Text should return a LeafNode with an "i" tag and the text
    if text_node.text_type == TextType.ITALIC:
        return LeafNode(tag = "i", props = {}, value = text_node.text)
    
    # Code Text should return a LeafNode with a "code" tag and the text
    if text_node.text_type == TextType.CODE:
        return LeafNode(tag = "code", props= {}, value=text_node.text)
    
    # Link Text should return a LeafNode with a "a" tag, anchor text and an "href" prop
    if text_node.text_type == TextType.LINK:
        return LeafNode(tag = "a", props = {"href":f"{text_node.url}"}, value = text_node.text)

    # Image Text should return a LeafNode with a "img" tag, empty string value, "src" and "alt" props
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(tag = "img", props = {"src":f"{text_node.url}", "alt":f"{text_node.text}"}, value="")
    
    else:
        raise ValueError("Unsupported text type: {}".format(text_node.text_type))


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes