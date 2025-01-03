from utils.copy import copy_from_to
from utils.generate_page import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():


    # 1 - Delete everything in the public directory and copy contents from static to public
    copy_from_to("./static", "./public")

    # 2 - Generate a page from content/index.md using template.html and write it to public/index.html
    generate_page()



if __name__ == "__main__":
    main()
