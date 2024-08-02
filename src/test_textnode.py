import unittest

from textnode import TextNode, text_type_bold, text_type_italic, text_type_text


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


if __name__ == "__main__":
    unittest.main()
