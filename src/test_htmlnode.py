import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props1 = {"href": "https://www.amazon.com", "target": "_blank"}
        props2 = {"href": "https://www.google.com"}
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), None)
        node1 = HTMLNode(props=props1)
        self.assertEqual(
            node1.props_to_html(), ' href="https://www.amazon.com" target="_blank"'
        )
        node2 = HTMLNode(props=props2)
        self.assertEqual(node2.props_to_html(), ' href="https://www.google.com"')


if __name__ == "__main__":
    unittest.main()
