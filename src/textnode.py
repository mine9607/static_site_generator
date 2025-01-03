import re
from enum import Enum
from htmlnode import HTMLNode, LeafNode
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
    return blocks

def block_to_block_type(block):
    # This function should return a string representing the type of block it is

    ''' Block types:
        paragraph
        heading
        code
        quote
        unordered_list
        ordered_list
    '''
    block_type = "paragraph"

    # Assume that all leading and trailing whitespace was already stripped

    if not block.strip():
         return block_type
    # Headings - start with 1 to 6 # characters followed by a space and then the heading text
    heading_match = re.match(r"^(#{1,6}) ", block)
    if heading_match:
        count = len(heading_match.group(1))
        block_type =f"heading{count}"

    # Code blocks - must start with (3) backticks and end with (3) backticks
    elif block.startswith("```") and block.endswith("```"):
        block_type = "code"

    else:
        # Split block into lines
        lines = block.split("\n")

        # Quote block - Every line must start with ">"
        if all(line.strip().startswith("> ") for line in lines if line.strip()):
            block_type = "quote"

        # Unordered list block - Every line must start with "- " or "* "
        elif all((line.strip().startswith("- ") or line.strip().startswith("* ")) for line in lines if line.strip()):
            block_type = "unordered_list"

        # Ordered list block - Each line must start with a number followed by ". "
        else:
            is_ordered_list = True
            expected_number = 1
            for line in lines:
                if line.strip():  # Skip empty lines
                    if not line.startswith(f"{expected_number}. "):
                        is_ordered_list = False
                        break
                    expected_number += 1

            if is_ordered_list:
                block_type = "ordered_list"

    # Return the determined block type
    return block_type

def get_block_content(block):
    # This function will remove the markdown delimiters and just return the text in the block

    block_type = block_to_block_type(block)
    
    content = "" 

    if block_type.startswith("heading"):
        pattern = r"^#{1,6} (.+)"
        match = re.match(pattern, block)
        if match:
            content = match.group(1).strip()
        
    elif block_type ==  "paragraph":
        content = block.strip()
    
    elif block_type == "quote":
        content = block.lstrip("> ").strip()

    elif block_type == "code":
        content = block[3:-3].strip()
    
    elif block_type in ["unordered_list", "ordered_list"]:
        lines = block.split('\n')
        content = [line.lstrip('-*0123456789. ').strip() for line in lines]

    return content

    
def markdown_block_to_html_string(block):
    block_type = block_to_block_type(block)

    content = get_block_content(block)

    html_string = ""

    if block_type == "paragraph":
        html_string = f"<p>{content}</p>"

    elif block_type == "heading":
        # count the number of "#" chars to determine the tag
        pattern = r"^(#+)"
        matches = re.findall(pattern, block[:6])
        if matches:
            count = len(matches[0])
        # now we can add the count to the header "<h3>"
        html_string = f"<h{count}>{content}</h{count}>"

    elif block_type == "quote":
        html_string = f"<blockquote>{content}</blockquote>"
    
    elif block_type == "code":
        html_string = f"<pre><code>{content}</code></pre>"

    elif block_type == "ordered_list":
        html_string = "<ol>"
        items = content
        for item in items:
            html_string += f"<li>{item}</li>"
        html_string += "</ol>"

    else:
        html_string = "<ul>"
        items = content
        for item in items:
            html_string += f"<li>{item}</li>"
        html_string += "</ul>"

    return html_string


def markdown_to_html_node(markdown):
    # Converts a full markdown doc to a single parent HTMLNode

    # That parent HTMLNode should contain many child HTMLNode objects
    root_node = HTMLNode(tag='div')

    # 1 - Split the markdown into blocks(use your function)
    blocks = markdown_to_blocks(markdown)

    if len(blocks) == 0:
        raise Exception("Invalid markdown - could not find blocks")

    # 2 - Loop over each block:
    for block in blocks:        
        # a. Determine the type of the block
        block_type = block_to_block_type(block)
        content = get_block_content(block)

        if block_type in ["unordered_list", "ordered_list"]:
            parent_node = HTMLNode('ul') if block_type == "unordered_list" else HTMLNode('ol')

            for list_item in content:
                child_node = HTMLNode('li')
                child_node.add_child(HTMLNode('text', value=list_item))
                parent_node.add_child(child_node)
            
            root_node.add_child(parent_node)
        
        else:
            # Handle as immediate leaf nodes like headings, paragraphs
            
            html_string = markdown_block_to_html_string(block)
            node = HTMLNode.from_string(html_string, block_type, content) #CREATE THIS FUNCTION
            root_node.add_child(node)
    return root_node
