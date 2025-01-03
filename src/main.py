from utils.copy import copy_from_to
from utils.extract_title import extract_title

def main():

    #copy_from_to("./static", "./public")

   title = extract_title("./content/index.md")
   #print(title)



if __name__ == "__main__":
    main()
