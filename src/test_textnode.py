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
if __name__ == "__main__":
    unittest.main()
