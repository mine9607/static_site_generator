import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_empty_node(self):
        # Test creating a LeafNode without providing required arguments
        with self.assertRaises(TypeError):
            node = LeafNode()  # Missing required 'tag' and 'props'

    def test_node_with_data(self):
        # Test creating a LeafNode with all required arguments
        node = LeafNode(
            tag="a",
            value="Link to Google",
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Link to Google")
        self.assertEqual(node.props, {"href": "https://www.google.com", "target": "_blank"})

    def test_props_to_html(self):
        # Test the props_to_html method
        node = LeafNode(
            tag="a",
            value="Link to Google",
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        expected_html = '<a href="https://www.google.com" target="_blank">Link to Google</a>'
        self.assertEqual(node.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()

