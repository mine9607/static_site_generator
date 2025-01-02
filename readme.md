# Build a Static Site Generator

A ssg takes raw content files (like markdown and images) and turns them into a static website

## Static vs Dynamic Sites:

Users cannot:
    - Upload files
    - Log in
    - Leave comments
    - Save preferences

HTML is a tree-like structure where each "tag" can contain other tags.

Static sites are good for:
    - Blogs
    - Portfolios
    - Landing pages
    - Documentation


## Architecture:
    1. Delete everything in the `/public` directory
    2. Copy any static assets (HTML template, images, CSS, etc.) to `/public` directory
    3. Generate an HTML file for each Markdown file in the `/content` directory
       
       For each Markdown file:
       1. Open the file and read its contents
       2. Split the markdown into "blocks" (e.g. paragraphs, headings, lists, etc.)
       3. Convert each block into a tree of `HTMLNode` objects:
            For each inline element (like bold text, links, etc.) we will convert:
                Raw markdown -> `TextNode` -> `HTMLNode`
       4. Join all the `HTMLNode` blocks under one large parent `HTMLNode` for the pages
       5. Use a recursive `to_html()` method to convert the `HTMLNode` and all its nested nodes 
          to a giant HTML string and inject it in the HTML template
       6. Write the full HTML string to a file for that page in the `/public` directory


## Steps to build SSG from Markdown:

This generator will take a dictionary Markdown files (one per webpage) and create a dictionary of
HTML files.

### Creating Nodes:

#### TextNode:

An intermediate representation of the text from the markdown file.

    - Normal text
    - Bold text
    - Italic text
    - Code text
    - Links
    - Images

We consider everything else block level (headings, paragraphs, and bullet lists)


 1. Create a TextType enum which defines the possible types that TextNodes can hold

 2. Create a `TextNode` class with 3 properties (text, text_type, url=None)

 3. Create a method `__eq__` that returns true if all properties of two TextNodes are equal

 4. Create a method `__repr__` that returns a string representation of the TextNode:
    `TextNode(TEXT, TEXT_TYPE, URL)`
 
 5. Add unit testing file with tests covering the properties and methods of the TextNode class

#### HTMLNode:

 A representation of a "node" in an HTML document tree (such as a <p> tag and its contents)

  1. Create a `htmlnode.py` file 

  2. Define the `HTMLNode` class with 4 properties (tag, value, children, props)
  
        - tag = a string representation of the HTML tag name ("p", "a", "h1", etc)
        - value = a string representing the value of the HTML tag (e.g. text inside a <p> tag)
        - children = a list of `HTMLNode` objects representing the children of this node
        - props = a dictionary of key:value pairs representing the `attributes` of the HTML tag.
            Ex: a link (<a> tag) should have {"href":"https://www.google.com"}

  3. Each member should be optional and default to `None`:
        * An HTMLNode without a tag will render as raw text
        * An HTMLNode without a value will be assumed to have children (defined in class methods)
        * An HTMLNode without children will be assumed to have a value (defined in class methods)
        * An HTMLNode without props simply won't have attributes

  4. Add a `to_html` method which raises a `NotImplementedError` - will be overridden by child classes

  5. Add a `props_to_html` method - It should return a string that represents the HTML attributes 
     of the node

     Ex: if self.props = {"href":"https://www.google.com", "target":"_blank"} then the returned string
         should look like: `href="https://www.google.com" target="_blank"` 

     Note the leading space before `href` and `target`

  6. Add a `__repr__` method to give return or print a string representation of the `HTMLNode` object
        
        - Useful for debugging

  7. Create some unittests for the `HTMLNode` class


#### LeafNode

  A type of `HTMLNode` that represents a single HTML tag with no children ("must have a value")

  1. In `htmlnode.py` create a child class of `HTMLNode` called `LeafNode`

  2. The `LeafNode` constructor should NOT ALLOW for any children

  3. The `LeafNode` value member MUST BE REQUIRED

        Ex: The LeafNode should have 3 properties (tag, value, props)
        Ex: The super.__init__(tag, value, [], props)  - need to pass an empty children list

  4. Use the super function to call the constructor of the `HTMLNode` class

  5. Add a `to_html` method that renders a leaf node as an HTML string (return a string)

        a. If the leaf node has no `value` raise a `ValueError`
        b. If there is no `tag` (e.g. its `None`) the `value` should be returned as raw text.
        c. Else render an HTML tag. for example:

            LeafNode("p", "This is a paragraph of text.")
            LeafNode("a", "Click me!", {"href": "https://www.google.com"})

           Should Render as:
            
            <p>This is a paragraph of text.</p>
            <a href="https://www.google.com">Click me!</a>

  6. Add unittests

#### ParentNode

The parent node class will handle the nesting of HTML nodes inside of one another.

Any HTML node that's not a "leaf" node (e.g. it has children) is a "parent node"

1. Create a subclass of `HTMLNode` called `ParentNode`

2. The `ParentNode` constructor MUST HAVE both `tag` and `children` properties

3. The `ParentNode` SHOULD NOT take a `value`

4. Add a `to_html` method that renders the parent node as an html string

    a. If the object doesn't have a `tag` property raise a `ValueError`
    b. If the object doesn't have a `children` property raise a `ValueError`
    c. Else return a string representing the HTML tag of the node AND its children

        This should be a recursive method (each recursion being called on a nested child node

        It should iterate over all the children and concatenate the resulting strings and injecting them between the opening and closing tags of the parent:

        Example:

        ```python
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        node.to_html()
       ``` 
       Should convert to:

       "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"


#### TextNode to HTMLNode

We need to convert a `TextNode` to an `HTMLNode` or specifically to a `LeafNode`

1. Write a function `text_node_to_html_node(text_node)` which should:

    - handle each type of the `TextType` enum.
    - if it gets a `TextNode` that is none of those types it should raise an Exception

        * `TextType.TEXT` should become a `LeafNode` with no tag, just a raw text value (string)
        * `TextType.BOLD` should become a `LeafNode` with a "b" tag and the text
        * `TextType.ITALIC` should become a `LeafNode` with a "i" tag and the text
        * `TextType.CODE` should become a `LeafNode` with a "code" tag and the text
        * `TextType.LINK` should become a `LeafNode` with a "a" tag, the text and "href" prop
        * `TextType.IMAGE` shoud become a `LeafNode` with a "img" tag, empty `value`, "src" and "alt" props
