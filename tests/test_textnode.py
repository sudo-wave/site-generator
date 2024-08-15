import unittest

import ssglite.constants as tt
from ssglite.nodes import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("General Node", tt.TEXT_TYPE_TEXT)
        node2 = TextNode("General Node", tt.TEXT_TYPE_TEXT)
        self.assertEqual(node1, node2)

    def test_eq_false(self):
        node1 = TextNode("General Node", tt.TEXT_TYPE_TEXT)
        node2 = TextNode("General Node", tt.TEXT_TYPE_BOLD)
        self.assertNotEqual(node1, node2)

    def test_eq_false2(self):
        node1 = TextNode("General Node", tt.TEXT_TYPE_TEXT)
        node2 = TextNode("Particular Node", tt.TEXT_TYPE_TEXT)
        self.assertNotEqual(node1, node2)

    def test_eq_false3(self):
        node1 = TextNode("General Node", tt.TEXT_TYPE_TEXT)
        node2 = TextNode("Particular Node", tt.TEXT_TYPE_BOLD)
        self.assertNotEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("General Node", tt.TEXT_TYPE_ITALIC, "https://www.google.com")
        node2 = TextNode("General Node", tt.TEXT_TYPE_ITALIC, "https://www.google.com")
        self.assertEqual(node1, node2)

    def test_eq_url_false(self):
        node1 = TextNode("General Node", tt.TEXT_TYPE_ITALIC, "https://www.google.com")
        node2 = TextNode("General Node", tt.TEXT_TYPE_ITALIC, "https://www.amazon.com")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node1 = TextNode("Test Node1", tt.TEXT_TYPE_TEXT, "https://www.youtube.com")
        self.assertEqual(
            "TextNode(Test Node1, text, https://www.youtube.com)", repr(node1)
        )
        node2 = TextNode("Test Node2", tt.TEXT_TYPE_BOLD, "https://www.google.com")
        self.assertEqual(
            "TextNode(Test Node2, bold, https://www.google.com)", repr(node2)
        )
        node3 = TextNode("Test Node3", tt.TEXT_TYPE_ITALIC, "https://www.netflix.com")
        self.assertEqual(
            "TextNode(Test Node3, italic, https://www.netflix.com)", repr(node3)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_TEXT_TYPE_BOLD(self):
        node = TextNode("Random text", tt.TEXT_TYPE_BOLD)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, "Random text")

    def test_text_type_code(self):
        node = TextNode("Random text", tt.TEXT_TYPE_CODE)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "code")
        self.assertEqual(leaf_node.value, "Random text")

    def test_text_type_image(self):
        node = TextNode("Random text", tt.TEXT_TYPE_IMAGE, "Random URL")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "img")
        self.assertEqual(leaf_node.value, "")
        self.assertEqual(leaf_node.props, {"src": "Random URL", "alt": "Random text"})

    def test_TEXT_TYPE_ITALIC(self):
        node = TextNode("Random text", tt.TEXT_TYPE_ITALIC)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "i")
        self.assertEqual(leaf_node.value, "Random text")

    def test_text_type_link(self):
        node = TextNode("Random text", tt.TEXT_TYPE_LINK, "Random URL")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "a")
        self.assertEqual(leaf_node.value, "Random text")
        self.assertEqual(leaf_node.props, {"href": "Random URL"})

    def test_TEXT_TYPE_TEXT(self):
        node = TextNode("Random text", tt.TEXT_TYPE_TEXT)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, None)
        self.assertEqual(leaf_node.value, "Random text")


if __name__ == "__main__":
    unittest.main()
