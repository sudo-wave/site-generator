import unittest

from main import split_nodes_link
from textnode import TextNode, text_type_link, text_type_text


class TestSplitLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
            "This is a link ![to youtube](https://www.youtube.com) and ![to netflix](https://www.netflix.com).",
            text_type_text,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("This is a link ", text_type_text),
                TextNode("to youtube", text_type_link, "https://www.youtube.com"),
                TextNode(" and ", text_type_text),
                TextNode("to netflix", text_type_link, "https://www.netflix.com"),
                TextNode(".", text_type_text),
            ],
        )


if __name__ == "__main__":
    unittest.main()
