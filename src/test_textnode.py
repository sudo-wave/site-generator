import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("General Node", "normal")
        node2 = TextNode("General Node", "normal")
        self.assertEqual(node1, node2)
        node3 = TextNode("General Node", "bold")
        node4 = TextNode("Particular Node", "normal")
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, node4)
        node5 = TextNode("General Node", "normal", "https://google.com")
        self.assertNotEqual(node1, node5)


if __name__ == "__main__":
    unittest.main()
