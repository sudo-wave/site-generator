import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props1 = {
            "class": "greeting",
            "href": "https://www.amazon.com",
            "target": "_blank",
        }
        props2 = {"class": "greeting", "href": "https://www.google.com"}
        node1 = HTMLNode("div", "Random text.", None, props1)
        self.assertEqual(
            node1.props_to_html(),
            ' class="greeting" href="https://www.amazon.com" target="_blank"',
        )
        node2 = HTMLNode("div", "Random text.", None, props2)
        self.assertEqual(
            node2.props_to_html(), ' class="greeting" href="https://www.google.com"'
        )

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_values(self):
        node = HTMLNode("div", "Random line of text.")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Random line of text.")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_empty_values(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("p", "Some text.", None, {"class": "primary"})
        self.assertEqual(
            repr(node), "HTMLNode(p, Some text., children: None, {'class': 'primary'})"
        )


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(
            "div", "A random line of text.", {"href": "https://www.google.com"}
        )
        self.assertEqual(
            node.to_html(),
            '<div href="https://www.google.com">A random line of text.</div>',
        )

    def test_to_html_no_props_with_tag(self):
        node = LeafNode("p", "One line of text.")
        self.assertEqual(node.to_html(), "<p>One line of text.</p>")

    def test_to_html_no_tag_with_props(self):
        node = LeafNode(None, "One line of text.", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "One line of text.")

    def test_to_html_no_tag_no_props(self):
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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        node = ParentNode("div", [child_node])
        self.assertEqual(node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        node = ParentNode("div", [child_node])
        self.assertEqual(
            node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        nested_node = ParentNode(
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
            nested_node.to_html(),
            "<div>First Level<span>Second Level<div>Third Level</div></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_no_children(self):
        node = ParentNode("p", [])
        self.assertEqual(node.to_html(), "<p></p>")

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
