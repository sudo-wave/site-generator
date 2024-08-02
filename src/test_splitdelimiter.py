import unittest

from main import split_nodes_delimiter
from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)


class TestLeafNode(unittest.TestCase):
    maxDiff = None

    def test_split_delimiter_return_list(self):
        node = TextNode("Text", text_type_text)
        self.assertTrue(
            isinstance(split_nodes_delimiter([node], "*", text_type_text), list)
        )

    def test_split_delimiter_text(self):
        node = TextNode("Regular text", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "*", text_type_text),
            [TextNode("Regular text", text_type_text)],
        )

    def test_split_delimiter_bold(self):
        node = TextNode("Text with a **bold** word", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "**", text_type_bold),
            [
                TextNode("Text with a ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word", text_type_text),
            ],
        )

    def test_split_delimiter_code(self):
        node = TextNode("Text with a `code block` word", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "`", text_type_code),
            [
                TextNode("Text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
        )

    def test_split_delimiter_italic(self):
        node = TextNode("Text with a *italicized* word", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "*", text_type_italic),
            [
                TextNode("Text with a ", text_type_text),
                TextNode("italicized", text_type_italic),
                TextNode(" word", text_type_text),
            ],
        )

    def test_split_delimiter_image(self):
        node = TextNode("Text with a image", text_type_image)
        self.assertEqual(
            split_nodes_delimiter([node], "*", text_type_italic),
            [TextNode("Text with a image", text_type_image)],
        )

    def test_split_delimiter_link(self):
        node = TextNode("Text with a link", text_type_link)
        self.assertEqual(
            split_nodes_delimiter([node], "*", text_type_italic),
            [TextNode("Text with a link", text_type_link)],
        )

    def test_split_delimiter_multiple_nodes(self):
        node1 = TextNode("One **bold** word", text_type_text)
        node2 = TextNode("One more **bold** word", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node1, node2], "**", text_type_bold),
            [
                TextNode("One ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word", text_type_text),
                TextNode("One more ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word", text_type_text),
            ],
        )


if __name__ == "__main__":
    unittest.main()
