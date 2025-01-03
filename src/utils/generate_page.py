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

