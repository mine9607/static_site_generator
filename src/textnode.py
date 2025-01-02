from enum import Enum
from htmlnode import LeafNode
from regex import extract_markdown_images, extract_markdown_links

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
    if len(old_nodes) == 0:
        new_nodes.append(TextNode("", TextType.TEXT))
        return new_nodes
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            # if sections[i] == "":
            #     continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_text_nodes(text):
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_image(nodes)
    
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split("\n\n") if block.strip()]
    print(blocks)
    return blocks