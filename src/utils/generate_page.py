import os

from markdown_blocks import markdown_to_html_node
from utils.extract_title import extract_title

def generate_page(from_path="content/index.md", dest_path="public/index.html", template_path="template.html"):
    """
    Generates an HTML page by replacing placeholders in a template with content
    from a markdown file and saves it to the specified destination.
    """

    # Validate paths
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"Source markdown file not found: {from_path}")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")

    # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    print(f"Generating page from '{from_path}' to '{dest_path}' using template '{template_path}'")

    # Read the markdown file
    with open(from_path, "r") as file:
        markdown = file.read()

    # Read the template file
    with open(template_path, "r") as file:
        template = file.read()

    # Convert markdown to HTML and extract title
    node = markdown_to_html_node(markdown)
    html = node.to_html()
    title = extract_title(markdown)

    # Replace placeholders in the template
    if "{{ Title }}" not in template or "{{ Content }}" not in template:
        raise ValueError("Template is missing required placeholders: {{Title}} or {{Content}}")

    new_template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Write the resulting HTML to the destination
    with open(dest_path, "w") as file:
        file.write(new_template)

    print(f"Page successfully generated at '{dest_path}'")

def generate_pages_recursive(content_dir_path="./content", template_path="./template.html", dest_dir_path="./public"):
    # Crawl every entry in the content directory
    # For each markdown file found, generate a new .html file using the same template.html
    # The generated pages should be written to the public directory in the same directory structure

    # crate abs paths to content directory and destination directory
    content_dir_path = os.path.abspath(content_dir_path)
    dest_dir_path = os.path.abspath(dest_dir_path)
    template_path = os.path.abspath(template_path)

    if not os.path.exists(content_dir_path):
        raise FileNotFoundError(f"Directory {content_dir_path} not found.  Please check path.")

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Couldn't find template file at {template_path}")

    if not os.path.exists(dest_dir_path):
        try:
            os.makedirs(dest_dir_path, exist_ok=True)
            print(f"Directory {dest_dir_path} created successfully.")
        except Exception as e:
            print(f"Failed to create destination directory {dest_dir_path}: {e}")
            raise
    
    # create the list of content dir objects:
    content_items = os.listdir(content_dir_path)

    if len(content_items)==0:
        print(f"Content directory at {content_dir_path} is empty.  Skipping...")
        return

    for item in content_items:
        # Create paths to source object and dir object
        item_src_path = os.path.join(content_dir_path,item)
        item_dest_path = os.path.join(dest_dir_path,item)
        
        # If the item is a file then call the generate_page() function
        if os.path.isfile(item_src_path):
            if item.endswith(".md"):
                item_dest_path = item_dest_path.replace(".md",".html")
                generate_page(item_src_path,item_dest_path, template_path=template_path)
        
        elif os.path.isdir(item_src_path):
            # If not an item then it is a directory and we call the generate_pages_recursive on the folder
            generate_pages_recursive(item_src_path, template_path=template_path, dest_dir_path=item_dest_path)
