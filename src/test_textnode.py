import unittest

from textnode import TextType, TextNode, text_node_to_html_node, split_nodes_delimiter, text_to_text_nodes
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        print("Testing if nodes are equal...\n")
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_repl(self):
        node = TextNode("This is a text node", TextType.CODE, "https://your-mom.com")
        self.assertEqual(node.__repr__(), 'TextNode(This is a text node, code, https://your-mom.com)')


class TestTextToHTMLFunc(unittest.TestCase):
    def setUp(self):
       # Create sample TextNode instances for testing
        self.normal_text_node = TextNode("Normal Text", TextType.TEXT)
        self.bold_text_node = TextNode("Bold Text", TextType.BOLD)
        self.italic_text_node = TextNode("Italic Text", TextType.ITALIC)
        self.code_text_node = TextNode("Code Text", TextType.CODE)
        self.link_text_node = TextNode("Link Text", TextType.LINK, url="https://example.com")
        self.image_text_node = TextNode("Image Alt Text", TextType.IMAGE, url="https://example.com/image.png") 

    def test_normal_text(self):
        text_node = TextNode("Sample text", TextType.TEXT)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "")
        self.assertEqual(result.value, "Sample text")
        self.assertEqual(result.props, {})

    def test_bold_text(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "b")
        self.assertEqual(result.value, "Bold text")
        self.assertEqual(result.props, {})

    def test_italic_text(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        result = text_node_to_html_node(text_node)
        self.assertIsInstance(result, LeafNode)
        self.assertEqual(result.tag, "i")
        self.assertEqual(result.value, "Italic text")
        self.assertEqual(result.props, {})

    def test_code_text(self):
        text_node = TextNode("Code snippet", TextType.CODE)
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
 
def test_split_nodes_delimiter(self):
    # Test 1: Node that isn't TextType.TEXT should pass through unchanged
    bold_node = TextNode("Bold Text", TextType.BOLD)
    result = split_nodes_delimiter([bold_node], "`", TextType.CODE)
    assert result == [bold_node]

    # Test 2: Basic delimiter split should work
    text_node = TextNode("This is `code` text", TextType.TEXT)
    result = split_nodes_delimiter([text_node], "`", TextType.CODE)
    expected = [
        TextNode("This is ", TextType.TEXT),
        TextNode("code", TextType.CODE),
        TextNode(" text", TextType.TEXT)
    ]
    assert result == expected

# class TestSplitNodesDelimiter(unittest.TestCase):
#     def test_node_not_text_type(self):
#         bold_node = TextNode("Bold Text", TextType.BOLD)
#         result = split_nodes_delimiter([bold_node], "`", TextType.CODE)
#         self.assertEqual(result, [bold_node])

#     def test_basic_delimiter_split(self):
#         text_node = TextNode("This is `code` text", TextType.TEXT)
#         result = split_nodes_delimiter([text_node], "`", TextType.CODE)
#         expected = [
#             TextNode("This is ", TextType.TEXT),
#             TextNode("code", TextType.CODE),
#             TextNode(" text", TextType.TEXT),
#         ]
#         self.assertEqual(result, expected)

#     def test_empty_nodes_list(self):
#         with self.assertRaises(ValueError):
#             split_nodes_delimiter([], "`", TextType.CODE)

#     def test_text_without_delimiter(self):
#         text_node = TextNode("This is plain text", TextType.TEXT)
#         with self.assertRaises(Exception):
#             split_nodes_delimiter([text_node], "`", TextType.CODE)

#     def test_multiple_delimiters_in_text(self):
#         text_node = TextNode("This is `code` and `more code`", TextType.TEXT)
#         with self.assertRaises(Exception):
#             split_nodes_delimiter([text_node], "`", TextType.CODE)

class TestTextToTextNodes(unittest.TestCase):
    def test_simple_text(self):
        # Test simple text with no formatting
        text = "This is plain text"
        result = text_to_text_nodes(text)
        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_bold_text(self):
        # Test text with bold formatting
        text = "This is **bold** text"
        result = text_to_text_nodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_italic_text(self):
        # Test text with italic formatting
        text = "This is *italic* text"
        result = text_to_text_nodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_code_block(self):
        # Test text with code block formatting
        text = "This is `code` text"
        result = text_to_text_nodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image(self):
        # Test text with an image
        text = "This is an ![image](https://example.com/image.jpg)"
        result = text_to_text_nodes(text)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
        ]
        self.assertEqual(result, expected)

    def test_link(self):
        # Test text with a link
        text = "This is a [link](https://example.com)"
        result = text_to_text_nodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_combined_formatting(self):
        # Test text with multiple types of formatting
        text = "This is **bold** and *italic* with a `code block` and a ![image](https://example.com/image.jpg) and a [link](https://example.com)"
        result = text_to_text_nodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and a ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_edge_case_no_formatting(self):
        # Test empty string
        text = ""
        result = text_to_text_nodes(text)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
