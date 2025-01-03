import unittest
from textnode import markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):
  def test_block_split(self):
    markdown = """
    # This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is the second list item\n* This is a third list item
    """
        
    blocks = markdown_to_blocks(markdown)

    expected = [
        "# This is a heading",
        "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
        "* This is the first list item in a list block\n* This is the second list item\n* This is a third list item",
    ]

    self.assertEqual(blocks, expected)

class TestBlockToBlockType(unittest.TestCase):

    def test_empty_blocks(self):
        """Test that empty blocks return 'paragraph'."""
        self.assertEqual(block_to_block_type(""), "paragraph")
        self.assertEqual(block_to_block_type("   "), "paragraph")
        self.assertEqual(block_to_block_type("\n\n"), "paragraph")

    def test_multiline_blocks_with_mixed_empty_lines(self):
        """Test blocks with mixed empty and non-empty lines."""
        block = "> Line 1\n\n> Line 2\n\n"
        self.assertEqual(block_to_block_type(block), "quote")

        block = "- Item 1\n\n- Item 2\n"
        self.assertEqual(block_to_block_type(block), "unordered_list")

        block = "1. First\n\n2. Second\n"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_edge_cases_for_headings(self):
        """Test heading blocks with different numbers of '#' characters."""
        self.assertEqual(block_to_block_type("# Heading 1"), "heading1")
        self.assertEqual(block_to_block_type("###### Heading 6"), "heading6")
        self.assertEqual(block_to_block_type("####### Invalid"), "paragraph")
        self.assertEqual(block_to_block_type("#NoSpaceAfter"), "paragraph")

    def test_malformed_ordered_lists(self):
        """Test ordered lists with incorrect numbering."""
        block = "1. First item\n3. Skipped second item\n2. Incorrect order"
        self.assertEqual(block_to_block_type(block), "paragraph")

        block = "1. First item\nSecond line without number\n2. Second item"
        self.assertEqual(block_to_block_type(block), "paragraph")

        block = "1. First item\n2 Second item missing dot"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_similar_looking_blocks(self):
      """Test blocks that look similar to other types."""
      block = "###This is not a heading"
      self.assertEqual(block_to_block_type(block), "paragraph")  # Missing space after '#'

      block = "-Item without space"
      self.assertEqual(block_to_block_type(block), "paragraph")  # Missing space after '-'

      block = ">Not a quote"
      self.assertEqual(block_to_block_type(block), "paragraph")  # Missing space after '>'

      block = "``` Incomplete code block"
      self.assertEqual(block_to_block_type(block), "paragraph")  # No closing backticks

      # Add a valid heading for verification
      block = "### Valid Heading"
      self.assertEqual(block_to_block_type(block), "heading3")  # Correct heading format

      # Add a valid quote block for verification
      block = "> Valid quote\n> Another valid line"
      self.assertEqual(block_to_block_type(block), "quote")  # Correct quote block format


class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraph(self):
        """Test a single paragraph block."""
        markdown = "This is a paragraph"
        node = markdown_to_html_node(markdown)

        # Check the root node
        self.assertEqual(node.tag, "div")  # Root node should be div
        self.assertEqual(len(node.children), 1)  # Should have one child

        # Check the paragraph node
        paragraph_node = node.children[0]
        self.assertEqual(paragraph_node.tag, "p")
        self.assertEqual(paragraph_node.value, "This is a paragraph")  # Check value

if __name__ == "__main__":
  unittest.main()
