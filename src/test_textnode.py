import unittest

from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import LeafNode

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
       # Create sample TextNode instances for testing
        self.normal_text_node = TextNode("Normal Text", TextType.NORMAL_TEXT)
        self.bold_text_node = TextNode("Bold Text", TextType.BOLD_TEXT)
        self.italic_text_node = TextNode("Italic Text", TextType.ITALIC_TEXT)
        self.code_text_node = TextNode("Code Text", TextType.CODE_TEXT)
        self.link_text_node = TextNode("Link Text", TextType.LINK, url="https://example.com")
        self.image_text_node = TextNode("Image Alt Text", TextType.IMAGE, url="https://example.com/image.png") 

    def test_normal_text(self):
        text_node = TextNode("Sample text", TextType.NORMAL_TEXT)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "")
        self.assertEqual(result.value, "Sample text")
        self.assertEqual(result.props, {})

    def test_bold_text(self):
        text_node = TextNode("Bold text", TextType.BOLD_TEXT)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "b")
        self.assertEqual(result.value, "Bold text")
        self.assertEqual(result.props, {})

    def test_italic_text(self):
        text_node = TextNode("Italic text", TextType.ITALIC_TEXT)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "i")
        self.assertEqual(result.value, "Italic text")
        self.assertEqual(result.props, {})

    def test_code_text(self):
        text_node = TextNode("Code snippet", TextType.CODE_TEXT)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "code")
        self.assertEqual(result.value, "Code snippet")
        self.assertEqual(result.props, {})

    def test_link_text(self):
        text_node = TextNode("Link text", TextType.LINK, url="http://example.com")
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "a")
        self.assertEqual(result.value, "Link text")
        self.assertEqual(result.props, {"href": "http://example.com"})

    def test_image_text(self):
        text_node = TextNode("Image alt text", TextType.IMAGE, url="http://example.com/image.jpg")
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "img")
        self.assertEqual(result.value, "")
        self.assertEqual(result.props, {"src": "http://example.com/image.jpg", "alt": "Image alt text"})

    def test_unsupported_text_type(self):
        text_node = TextNode("Unsupported text", "unsupported")
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(
            str(context.exception), "Unsupported text type: unsupported"
        )
 


if __name__ == "__main__":
    unittest.main()
