
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []  # Default to an empty list if no children are provided
        self.props = props or {}        # Default to an empty dictionary if no props are provided

    def to_html(self):
        raise NotImplementedError("Child classes will override this method to render themselves as HTML")

    def props_to_html(self):
        props_list = [f' {key}="{value}"' for key, value in self.props.items()]
        return "".join(props_list)

    def __repr__(self):
        return (
            f"HTMLNode:\n"
            f"\tTag: {self.tag}\n"
            f"\tValue: {self.value}\n"
            f"\tChildren: {self.children}\n"
            f"\tProps: {self.props}"
        )
    
    def add_child(self, child_node):
        self.children.append(child_node)

    @staticmethod
    def from_string(html_string, block_type, content):
        if block_type == "paragraph":
            return HTMLNode(tag="p", value=content)

        elif block_type.startswith("heading"):
            # Extract the heading level from the block type (e.g., "heading1", "heading2")
            level = block_type[-1]  # Assuming block_type format is "heading1", "heading2", etc.
            return HTMLNode(tag=f"h{level}", value=content)

        elif block_type == "code":
            code_node = HTMLNode(tag="code", value=content)
            return HTMLNode(tag="pre", children=[code_node])
        
        elif block_type == "quote":
            return HTMLNode(tag="blockquote", value=content)

        return HTMLNode(tag="div", value=content)

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent nodes require a tag property")
        if self.children is None:
            raise ValueError("Parent nodes require a children property")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, props, value=None):
        super().__init__(tag, value,[], props)

        if value == None and tag != "img":
            raise ValueError("Leaf nodes require a value property")


    def to_html(self):
        if not self.tag:
            return self.value

        open_tag = f"<{self.tag}{self.props_to_html()}>"
        close_tag = f"</{self.tag}>"

        if self.tag == "img":
            return open_tag
        return f"{open_tag}{self.value}{close_tag}"
        # method should render the leaf node as an HTML string (returns a string)


