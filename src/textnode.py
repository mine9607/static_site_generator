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


def split_nodes_delimiter(old_nodes:list, delimiter, text_type:TextType):
    # Code should accept a list of nodes, a delimiter and a text_type and for each TextNode:
        # split the node on the delimiter:
            # text before the delimiter should be of type TextNode.TEXT
            # text between the delimiter should be of type defined by delimiter (.BOLD, .ITALIC, .CODE)
            # text after the delimiter should be of type TextNode.TEXT
        
        # returns a list of lists if len(old_nodes) >1 or a list if len(old_nodes) == 1

    ''' TIPS 
        1 - if an "old_node" is not a TextType.TEXT type then just add it to the list of new nodes "as-is"
        2 - if a matching closing delimiter is not found then 
    '''

    # create a new list to append to:
    new_nodes = []


    #check if node list is empty and if so raise an exception
    if len(old_nodes)==0:
        raise ValueError("Nodes parameter much contain a list with at least one node")


    for node in old_nodes:
        # if nodes text_type isn't TextType.TEXT then append to new_nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

        else:
            # check if trailing delimiter found len of split node would be <3
            parts = node.text.split(delimiter)
            if len(parts) < 3 :
                raise Exception("Missing matching delimiters please check TextNode.text")
            if len(parts) > 3 :
                raise Exception("TextNode.text contains multiple delimiters which is not allowed!")
            else:
                # Assign the TextType.Text to the leading and trailing string splits
                before = TextNode(parts[0], TextType.TEXT)
                between = TextNode(parts[1], text_type)
                end = TextNode(parts[2], TextType.TEXT)

                ## Note: we may need to create new TextNodes from the splits since the split is likely just createing the strings
                new_nodes.extend([before, between, end])

    return new_nodes