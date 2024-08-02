import unittest

from textnode import (
    TextNode,
    text_node_to_html_node,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("General Node", text_type_text)
        node2 = TextNode("General Node", text_type_text)
        self.assertEqual(node1, node2)

    def test_eq_false(self):
        node1 = TextNode("General Node", text_type_text)
        node2 = TextNode("General Node", text_type_bold)
        self.assertNotEqual(node1, node2)

    def test_eq_false2(self):
        node1 = TextNode("General Node", text_type_text)
        node2 = TextNode("Particular Node", text_type_text)
        self.assertNotEqual(node1, node2)

    def test_eq_false3(self):
        node1 = TextNode("General Node", text_type_text)
        node2 = TextNode("Particular Node", text_type_bold)
        self.assertNotEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("General Node", text_type_italic, "https://www.google.com")
        node2 = TextNode("General Node", text_type_italic, "https://www.google.com")
        self.assertEqual(node1, node2)

    def test_eq_url_false(self):
        node1 = TextNode("General Node", text_type_italic, "https://www.google.com")
        node2 = TextNode("General Node", text_type_italic, "https://www.amazon.com")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node1 = TextNode("Test Node1", text_type_text, "https://www.youtube.com")
        self.assertEqual(
            "TextNode(Test Node1, text, https://www.youtube.com)", repr(node1)
        )
        node2 = TextNode("Test Node2", text_type_bold, "https://www.google.com")
        self.assertEqual(
            "TextNode(Test Node2, bold, https://www.google.com)", repr(node2)
        )
        node3 = TextNode("Test Node3", text_type_italic, "https://www.netflix.com")
        self.assertEqual(
            "TextNode(Test Node3, italic, https://www.netflix.com)", repr(node3)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_type_bold(self):
        node = TextNode("Random text", text_type_bold)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, "Random text")

    def test_text_type_code(self):
        node = TextNode("Random text", text_type_code)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "code")
        self.assertEqual(leaf_node.value, "Random text")

    def test_text_type_image(self):
        node = TextNode("Random text", text_type_image, "Random URL")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "img")
        self.assertEqual(leaf_node.value, "")
        self.assertEqual(leaf_node.props, {"src": "Random URL", "alt": "Random text"})

    def test_text_type_italic(self):
        node = TextNode("Random text", text_type_italic)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "i")
        self.assertEqual(leaf_node.value, "Random text")

    def test_text_type_link(self):
        node = TextNode("Random text", text_type_link, "Random URL")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "a")
        self.assertEqual(leaf_node.value, "Random text")
        self.assertEqual(leaf_node.props, {"href": "Random URL"})

    def test_text_type_text(self):
        node = TextNode("Random text", text_type_text)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, None)
        self.assertEqual(leaf_node.value, "Random text")


if __name__ == "__main__":
    unittest.main()
