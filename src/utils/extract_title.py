
from textnode import markdown_to_blocks, block_to_block_type, get_block_content

def extract_title(markdown_path):
    # function should find the h1 header and return just its contents
    # if there is no h1 raise an exception
    # strip any leading or trailing whitespace

    ''' NOTE -- will need a function to read the markdown file path and return the contents to pass to this func
    print('START EXTRACT TITLE')
    markdown_content = ''
    with open(markdown_path, "r") as file:
        markdown_content = file.read()
    '''
    
    title = ""
    blocks = markdown_to_blocks(markdown_content)

    block_types = [];
    for block in blocks[:3]:
        block_type = block_to_block_type(block)
        block_types.append(block_type)
        
        if block_type == "heading1":
            title = get_block_content(block).strip()

    if len(block_types)==0:
        raise Exception("No header found")
    return title
