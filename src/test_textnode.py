import unittest

from textnode import TextType, TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        print("Testing if nodes are equal...\n")
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    
    def test_repl(self):
        node = TextNode("This is a text node", TextType.CODE_TEXT, "https://your-mom.com")
        self.assertEqual(node.__repr__(), 'TextNode(This is a text node, code, https://your-mom.com)')


class TestTextToHTMLFunc(unittest.TestCase):
    def setUp(self):
        self.TextType = Mock()  # Mock the TextType enumeration or class
        self.TextType.NORMAL_TEXT = "normal"
        self.TextType.BOLD_TEXT = "bold"
        self.TextType.ITALIC_TEXT = "italic"
        self.TextType.CODE_TEXT = "code"
        self.TextType.LINK = "link"
        self.TextType.IMAGE = "image"

    def test_normal_text(self):
        text_node = Mock()
        text_node.text_type = self.TextType.NORMAL_TEXT
        text_node.text = "Sample text"
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, htmlnode.LeafNode)
        self.assertEqual(result.tag, "")
        self.assertEqual(result.value, "Sample text")
        self.assertEqual(result.props, {})

    def test_bold_text(self):
        text_node = Mock()
        text_node.text_type = self.TextType.BOLD_TEXT
        text_node.text = "Bold text"
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, htmlnode.LeafNode)
        self.assertEqual(result.tag, "b")
        self.assertEqual(result.value, "Bold text")
        self.assertEqual(result.props, {})

    def test_italic_text(self):
        text_node = Mock()
        text_node.text_type = self.TextType.ITALIC_TEXT
        text_node.text = "Italic text"
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, htmlnode.LeafNode)
        self.assertEqual(result.tag, "i")
        self.assertEqual(result.value, "Italic text")
        self.assertEqual(result.props, {})

    def test_code_text(self):
        text_node = Mock()
        text_node.text_type = self.TextType.CODE_TEXT
        text_node.text = "Code snippet"
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, htmlnode.LeafNode)
        self.assertEqual(result.tag, "code")
        self.assertEqual(result.value, "Code snippet")
        self.assertEqual(result.props, {})

    def test_link_text(self):
        text_node = Mock()
        text_node.text_type = self.TextType.LINK
        text_node.text = "Link text"
        text_node.url = "http://example.com"
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, htmlnode.LeafNode)
        self.assertEqual(result.tag, "a")
        self.assertEqual(result.value, "Link text")
        self.assertEqual(result.props, {"href": "http://example.com"})

    def test_image_text(self):
        text_node = Mock()
        text_node.text_type = self.TextType.IMAGE
        text_node.text = "Image alt text"
        text_node.url = "http://example.com/image.jpg"
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, htmlnode.LeafNode)
        self.assertEqual(result.tag, "img")
        self.assertEqual(result.value, "")
        self.assertEqual(result.props, {"src": "http://example.com/image.jpg", "alt": "Image alt text"})

    def test_unsupported_text_type(self):
        text_node = Mock()
        text_node.text_type = "unsupported"
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(
            str(context.exception), "Unsupported text type: unsupported"
        )


if __name__ == "__main__":
    unittest.main()
