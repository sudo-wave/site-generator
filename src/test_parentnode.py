import unittest

from htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html(self):

        node = ParentNode(
            "div",
            [
                LeafNode(
                    "a",
                    "The reference for this node is google",
                    {"href": "https://www.google.com"},
                ),
                LeafNode(
                    "a",
                    "Some random text",
                    {"href": "https://www.amazon.com", "target": "_blank"},
                ),
                LeafNode(None, "Some random text again"),
            ],
            {"href": "https://www.netflix.com"},
        )
        self.assertEqual(
            node.to_html(),
            '<div href="https://www.netflix.com"><a href="https://www.google.com">The reference for this node is google</a><a href="https://www.amazon.com" target="_blank">Some random text</a>Some random text again</div>',
        )

    def test_to_html_nested_parent_nodes(self):
        node = ParentNode(
            "div",
            [
                LeafNode(None, "First Level"),
                ParentNode(
                    "span",
                    [
                        LeafNode(None, "Second Level"),
                        ParentNode("div", [LeafNode(None, "Third Level")]),
                    ],
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div>First Level<span>Second Level<div>Third Level</div></span></div>",
        )

    def test_to_html_multiple_children(self): ...

    def test_to_html_no_children(self):
        node = ParentNode("p", [])
        self.assertEqual(node.to_html(), "<p></p>")


if __name__ == "__main__":
    unittest.main()
