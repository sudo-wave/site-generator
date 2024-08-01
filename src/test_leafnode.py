import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        try:
            node_empty = LeafNode()
        except TypeError:
            pass
        else:
            raise AssertionError("TypeError was not raised")
        props1 = {"href": "https://www.amazon.com", "target": "_blank"}
        props2 = {"href": "https://www.google.com"}
        node_no_value = LeafNode(None)
        try:
            node_no_value.to_html()
        except ValueError:
            pass
        else:
            raise AssertionError("ValueError was not raised")
        node_no_tag_no_value = LeafNode(value="Some text")
        self.assertEqual(node_no_tag_no_value.to_html(), "Some text")
        node_no_tag = LeafNode(value="More text", props=props1)
        self.assertEqual(node_no_tag.to_html(), "More text")
        node_no_value = LeafNode(value="Even more text", tag="p")
        self.assertEqual(node_no_value.to_html(), "<p>Even more text</p>")
        node = LeafNode(value="Short line of text.", tag="a", props=props2)
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Short line of text.</a>'
        )


if __name__ == "__main__":
    unittest.main()
