import unittest

from main import split_nodes_image
from textnode import TextNode, text_type_image, text_type_text


class TestSplitImage(unittest.TestCase):
    maxDiff = None
    node = TextNode(
        "This is text with an image [cat image](https://imgur.com/cat.png) and another image [dog gif](https://imgur.com/dog.gif)",
        text_type_text,
    )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is a ![cat image](https://imgur.com/cat.png) and a ![dog gif](https://imgur.com/dog.gif)!",
            text_type_text,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("This is a ", text_type_text),
                TextNode("cat image", text_type_image, "https://imgur.com/cat.png"),
                TextNode(" and a ", text_type_text),
                TextNode("dog gif", text_type_image, "https://imgur.com/dog.gif"),
                TextNode("!", text_type_text),
            ],
        )


if __name__ == "__main__":
    unittest.main()
