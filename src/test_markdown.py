import unittest
from textnode import markdown_to_blocks

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

if __name__ == "__main__":
  unittest.main()
