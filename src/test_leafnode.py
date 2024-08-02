import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(
            "div", "A random line of text.", {"href": "https://www.google.com"}
        )
        self.assertEqual(
            node.to_html(),
            '<div href="https://www.google.com">A random line of text.</div>',
        )

    def test_to_html_no_props(self):
        node = LeafNode("p", "One line of text.")
        self.assertEqual(node.to_html(), "<p>One line of text.</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "One line of text.", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "One line of text.")

    def test_to_html_no_tag_props(self):
        node = LeafNode(None, "One line of text.")
        self.assertEqual(node.to_html(), "One line of text.")

    def test_to_html_no_value(self):
        node = LeafNode(None, None)
        try:
            node.to_html()
        except ValueError:
            pass
        else:
            raise AssertionError("ValueError was not raised")

    def test_repr(self):
        node = LeafNode("p", "Text", {"href": "https://www.amazon.com"})
        self.assertEqual(
            "LeafNode(p, Text, {'href': 'https://www.amazon.com'})", repr(node)
        )


if __name__ == "__main__":
    unittest.main()
