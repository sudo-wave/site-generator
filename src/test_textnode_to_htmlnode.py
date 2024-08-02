import unittest

from htmlnode import *
from main import text_node_to_html_node
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
    def test_text_node_to_html_node(self):
        node = TextNode("Random text", text_type_text, "Random url")
        self.assertTrue(isinstance(text_node_to_html_node(node), LeafNode))

    def test_text_type_bold(self):
        node = TextNode("Random text", text_type_bold)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.get_tag(), "b")
        self.assertEqual(leaf_node.get_value(), "Random text")

    def test_text_type_code(self):
        node = TextNode("Random text", text_type_code)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.get_tag(), "code")
        self.assertEqual(leaf_node.get_value(), "Random text")

    def test_text_type_image(self):
        node = TextNode("Random text", text_type_image, "Random URL")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.get_tag(), "img")
        self.assertEqual(leaf_node.get_value(), "")
        self.assertEqual(
            leaf_node.get_props(), {"src": "Random URL", "alt": "Random text"}
        )

    def test_text_type_italic(self):
        node = TextNode("Random text", text_type_italic)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.get_tag(), "i")
        self.assertEqual(leaf_node.get_value(), "Random text")

    def test_text_type_link(self):
        node = TextNode("Random text", text_type_link, "Random URL")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.get_tag(), "a")
        self.assertEqual(leaf_node.get_value(), "Random text")
        self.assertEqual(leaf_node.get_props(), {"href": "Random URL"})

    def test_text_type_text(self):
        node = TextNode("Random text", text_type_text)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.get_tag(), None)
        self.assertEqual(leaf_node.get_value(), "Random text")


if __name__ == "__main__":
    unittest.main()
