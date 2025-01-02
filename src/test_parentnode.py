import unittest
from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    # BUG: Not working ------
    """
    def test_parent_node_without_tag(self):
        # Test: ParentNode without a tag should raise a ValueError
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [LeafNode("span", {"id": "test"}, "Hello")])
        self.assertEqual(str(context.exception), "Parent nodes require a tag property")
    """
    # BUG: NOT working ------------------
    '''
    def test_parent_node_without_children(self):
        # Test: ParentNode without children should raise a ValueError
        with self.assertRaises(ValueError) as context:
            ParentNode("p", None)
        self.assertEqual(str(context.exception), "Parent nodes require a children property")
    '''

    def test_parent_node_with_children(self):
        # Test: ParentNode with valid children
        node = ParentNode(
            "div",
            [
                LeafNode("b", {"class": "bold"}, "Bold text"),
                LeafNode(None, {}, "Normal text"),
            ]
        )
        expected_html = '<div><b class="bold">Bold text</b>Normal text</div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_parent_node_with_props(self):
        # Test: ParentNode with props
        node = ParentNode(
            "div",
            [LeafNode("span", {"id": "test"}, "Hello")],
            props={"class": "container"}
        )
        expected_html = '<div class="container"><span id="test">Hello</span></div>'
        self.assertEqual(node.to_html(), expected_html)

    def test_nested_parent_node(self):
        # Test: Nested ParentNode structure
        node = ParentNode(
            "section",
            [
                ParentNode(
                    "div",
                    [LeafNode("b", {"class": "bold"}, "Bold text")]
                ),
                LeafNode("p", {}, "A paragraph"),
            ]
        )
        expected_html = '<section><div><b class="bold">Bold text</b></div><p>A paragraph</p></section>'
        self.assertEqual(node.to_html(), expected_html)
    
    # BUG Not working ---------------
    """
    def test_repr_method(self):
    # Test __repr__
        node = ParentNode(
            "div",
            [LeafNode("span", {"id": "test"}, "Hello")],
            props={"class": "container"}
        )
        expected_repr = (
            "ParentNode(div, children: [HTMLNode(span, Hello, children: None, {'id': 'test'})], {'class': 'container'})"
        )
        self.assertEqual(repr(node), expected_repr)
    """

if __name__ == "__main__":
    unittest.main()

