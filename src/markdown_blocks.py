from htmlnode import ParentNode
from inline_markdown import text_to_text_nodes
from textnode import text_node_to_html_node


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    ''' Block types:
        paragraph
        heading
        code
        quote
        unordered_list
        ordered_list
    '''
    block_lines = block.split("\n")
    block_type = "paragraph"

    # Assume that all leading and trailing whitespace was already stripped

    # Headings:
    # start with 1 to 6 # characters followed by a space and then the heading text
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        block_type = "heading"

    # Code blocks:
    # must start with (3) backticks and end with (3) backticks
    if len(block_lines) > 1 and block_lines[0].startswith("```") and block_lines[-1].startswith("```"):
        block_type = "code"

     # Quote block - Every line must start with ">"
     if block.startswith(">"):
         for line in block_lines:
             if not line.startwsith(">"):
                 block_type = "paragraph"
         block_type = "quote"

     # Unordered List
     if block.startswith("* "):
         for line in block_lines:
             if not line.startswith("* "):
                 block_type = "paragraph"
         block_type = "unordered_list"

     if block.startswith("- "):
         for line in block_lines:
             if not line.startswith("- "):
                 block_type = "paragraph"
         block_type = "unordered_list"

     # Ordered List
     if block.startswith("1. "):
         i = 1
         for line in block_lines:
             if not line.startswith(f"{i}. "):
                 block_type = "paragraph
             i += 1
         block_type = "ordered_list"
    block_type = "paragraph"

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
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    
    if block_type == "paragraph":
        return paragraph_to_html_node(block)

    if block_type[:6] == "heading":
        return heading_to_html_node(block)
    if block_type == "code":
        return code_to_html_node(block)
    if block_type == "ordered_list":
        return olist_to_html_node(block)
    if block_type == "unordered_list":
        return ulist_to_html_node(block)
    if block_type == "quote":
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
        level += 1
    else:
        break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startwsith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
