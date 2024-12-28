import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_empty_node(self):
        print("Testing empty node...\n")
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props,{})

    def test_node_with_data(self):
        print("Testing node with data members...\n")
        node = HTMLNode("a", "Link to Google",[] ,{"href":"https://www.google.com", "target":"_blank"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Link to Google")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"href":"https://www.google.com", "target":"_blank" })
    
    def test_props_to_html(self):

        print("Testing props_to_html method...\n")
        node = HTMLNode("a", "Link to Google",[] ,{"href":"https://www.google.com", "target":"_blank"})
        
        expected_props = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_props)
        print(node.props_to_html())

if __name__ == "__main__":
    unittest.main()
