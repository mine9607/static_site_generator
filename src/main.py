from utils.copy import copy_from_to
from utils.generate_page import generate_pages_recursive, generate_page
from utils.extract_title import extract_title

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():

    #extract_title("./content/index.md")
    # 1 - Delete everything in the public directory and copy contents from static to public
    #copy_from_to("./static", "./public")

    # 2 - Generate a page from content/index.md using template.html and write it to public/index.html
    generate_pages_recursive(dir_path_content,template_path, dir_path_public) 


if __name__ == "__main__":
    main()
