import re

def extract_markdown_images(text):
  # accepts raw markdown text and returns a list of tuples
  # each tuple should contain the alt_text and URL of any markdown images

  '''Pattern between HTML and Markdown
    Markdown: ![alt text for image](url/of/image.jpg)
    HTML: <img src="url/of/image.jpg" alt="Description of image">
  '''

  ''' Below: First Attempt - works but not ideal
        alt_text = re.findall(r"\[(.*?)\]")
        url = re.findall(r"\((.*?)\)")

        results = list(zip(alt_text, url))

        return (alt_text,url)
  '''

  pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  return matches


def extract_markdown_links(text):
  # accepts raw markdown text and returns a list of tuples
  # each tuple should contain the anchor text and the src (url)

  ''' Pattern between HTML and Markdown
    Markdown: [link](https://www.google.com)
    HTML: <a href="https://www.google.com">link</a>
  '''
  # (?<!!) = no preceeding ! becuase that would be an image
  # \[ = escape the special character of regex and INCLUDE "[" in the match
  # () = a capture group defining the pattern of characters to include
  # ([]) = [] defines the character set to match and store in the surrounding capture group
  # ([^\[\]]*) = ^\[\] = do not match "[" or "]" inside the character set but match anything else
  #                     any "[" or "]" will end the pattern match and return the characters found
  #  
  pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  
  return matches