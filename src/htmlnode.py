
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
