import unittest

import ssglite.constants as tt
from ssglite.parser import (
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        file = """
This is a **bolded** word.

This is a paragraph with an *italic* word and `code` here.
This is the same paragraph on a new line.

* First item on a list
* Second item on a list
"""
        blocks = markdown_to_blocks(file)
        self.assertEqual(
            [
                "This is a **bolded** word.",
                "This is a paragraph with an *italic* word and `code` here.\nThis is the same paragraph on a new line.",
                "* First item on a list\n* Second item on a list",
            ],
            blocks,
        )

    def test_markdown_to_blocks_newlines(self):
        file = """
This is a **bolded** word.




This is a paragraph with an *italic* word and `code` here.
This is the same paragraph on a new line.

* First item on a list
* Second item on a list
"""
        blocks = markdown_to_blocks(file)
        self.assertEqual(
            blocks,
            [
                "This is a **bolded** word.",
                "This is a paragraph with an *italic* word and `code` here.\nThis is the same paragraph on a new line.",
                "* First item on a list\n* Second item on a list",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), tt.BLOCK_TYPE_HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), tt.BLOCK_TYPE_CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), tt.BLOCK_TYPE_QUOTE)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), tt.BLOCK_TYPE_UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), tt.BLOCK_TYPE_ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), tt.BLOCK_TYPE_PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
