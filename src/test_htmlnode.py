import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
