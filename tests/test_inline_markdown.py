import unittest

import ssglite.constants as tt
from ssglite.nodes import TextNode
from ssglite.parser import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
)


class TestSplitDelimiter(unittest.TestCase):
    def test_split_delimiter_return_list(self):
        node = TextNode("Text", tt.TEXT_TYPE_TEXT)
        self.assertTrue(
            isinstance(split_nodes_delimiter([node], "*", tt.TEXT_TYPE_TEXT), list)
        )

    def test_split_delimiter_text(self):
        node = TextNode("Regular text", tt.TEXT_TYPE_TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "*", tt.TEXT_TYPE_TEXT),
            [TextNode("Regular text", tt.TEXT_TYPE_TEXT)],
        )

    def test_split_delimiter_bold(self):
        node = TextNode("This is text with a **bolded** word", tt.TEXT_TYPE_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", tt.TEXT_TYPE_BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", tt.TEXT_TYPE_TEXT),
                TextNode("bolded", tt.TEXT_TYPE_BOLD),
                TextNode(" word", tt.TEXT_TYPE_TEXT),
            ],
            new_nodes,
        )

    def test_split_delimiter_code(self):
        node = TextNode("Text with a `code block` word", tt.TEXT_TYPE_TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", tt.TEXT_TYPE_CODE),
            [
                TextNode("Text with a ", tt.TEXT_TYPE_TEXT),
                TextNode("code block", tt.TEXT_TYPE_CODE),
                TextNode(" word", tt.TEXT_TYPE_TEXT),
            ],
        )

    def test_split_delimiter_italic(self):
        node = TextNode("Text with a *italicized* word", tt.TEXT_TYPE_TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "*", tt.TEXT_TYPE_ITALIC),
            [
                TextNode("Text with a ", tt.TEXT_TYPE_TEXT),
                TextNode("italicized", tt.TEXT_TYPE_ITALIC),
                TextNode(" word", tt.TEXT_TYPE_TEXT),
            ],
        )

    def test_split_delimiter_image(self):
        node = TextNode("Text with a image", tt.TEXT_TYPE_IMAGE)
        self.assertEqual(
            split_nodes_delimiter([node], "*", tt.TEXT_TYPE_ITALIC),
            [TextNode("Text with a image", tt.TEXT_TYPE_IMAGE)],
        )

    def test_split_delimiter_link(self):
        node = TextNode("Text with a link", tt.TEXT_TYPE_LINK)
        self.assertEqual(
            split_nodes_delimiter([node], "*", tt.TEXT_TYPE_ITALIC),
            [TextNode("Text with a link", tt.TEXT_TYPE_LINK)],
        )

    def test_split_delimiter_double_bold(self):
        node = TextNode(
            "One **bold** word and one more **bold** word", tt.TEXT_TYPE_TEXT
        )
        self.assertEqual(
            split_nodes_delimiter([node], "**", tt.TEXT_TYPE_BOLD),
            [
                TextNode("One ", tt.TEXT_TYPE_TEXT),
                TextNode("bold", tt.TEXT_TYPE_BOLD),
                TextNode(" word and one more ", tt.TEXT_TYPE_TEXT),
                TextNode("bold", tt.TEXT_TYPE_BOLD),
                TextNode(" word", tt.TEXT_TYPE_TEXT),
            ],
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**Bold** and *Italic*", tt.TEXT_TYPE_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", tt.TEXT_TYPE_BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", tt.TEXT_TYPE_ITALIC)
        self.assertListEqual(
            [
                TextNode("Bold", tt.TEXT_TYPE_BOLD),
                TextNode(" and ", tt.TEXT_TYPE_TEXT),
                TextNode("Italic", tt.TEXT_TYPE_ITALIC),
            ],
            new_nodes,
        )


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![image](https://i.imgur.com/aKaOqIh.gif) and ![another image](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("image", "https://i.imgur.com/aKaOqIh.gif"),
                ("another image", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.netflix.com) and [another link](https://www.youtube.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("link", "https://www.netflix.com"),
                ("another link", "https://www.youtube.com"),
            ],
        )


class TestSplitImages(unittest.TestCase):
    def test_split_nodes_single_image(self):
        node = TextNode("![image](https://i.imgur.com/zAV93b)", tt.TEXT_TYPE_TEXT)
        self.assertEqual(
            split_nodes_images([node]),
            [TextNode("image", tt.TEXT_TYPE_IMAGE, "https://i.imgur.com/zAV93b")],
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is a ![image](https://i.imgur.com/zAV93b)", tt.TEXT_TYPE_TEXT
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode("This is a ", tt.TEXT_TYPE_TEXT),
                TextNode("image", tt.TEXT_TYPE_IMAGE, "https://i.imgur.com/zAV93b"),
            ],
        )

    def test_split_nodes_images(self):
        node = TextNode(
            "This is a ![cat image](https://imgur.com/cat.png) and a ![dog gif](https://imgur.com/dog.gif)!",
            tt.TEXT_TYPE_TEXT,
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode("This is a ", tt.TEXT_TYPE_TEXT),
                TextNode("cat image", tt.TEXT_TYPE_IMAGE, "https://imgur.com/cat.png"),
                TextNode(" and a ", tt.TEXT_TYPE_TEXT),
                TextNode("dog gif", tt.TEXT_TYPE_IMAGE, "https://imgur.com/dog.gif"),
                TextNode("!", tt.TEXT_TYPE_TEXT),
            ],
        )


class TestSplitLinks(unittest.TestCase):
    def test_split_nodes_single_link(self):
        node = TextNode("[link](https://www.google.com)", tt.TEXT_TYPE_TEXT)
        self.assertEqual(
            split_nodes_links([node]),
            [TextNode("link", tt.TEXT_TYPE_LINK, "https://www.google.com")],
        )

    def test_split_nodes_link(self):
        node = TextNode("This is a [link](https://www.netflix.com)", tt.TEXT_TYPE_TEXT)
        self.assertEqual(
            split_nodes_links([node]),
            [
                TextNode("This is a ", tt.TEXT_TYPE_TEXT),
                TextNode("link", tt.TEXT_TYPE_LINK, "https://www.netflix.com"),
            ],
        )

    def test_split_nodes_links(self):
        node = TextNode(
            "This is a [link](https://www.amazon.com) and a [another link](https://www.pinterest.com)",
            tt.TEXT_TYPE_TEXT,
        )
        self.assertEqual(
            split_nodes_links([node]),
            [
                TextNode("This is a ", tt.TEXT_TYPE_TEXT),
                TextNode("link", tt.TEXT_TYPE_LINK, "https://www.amazon.com"),
                TextNode(" and a ", tt.TEXT_TYPE_TEXT),
                TextNode(
                    "another link", tt.TEXT_TYPE_LINK, "https://www.pinterest.com"
                ),
            ],
        )


class TestTextToNode(unittest.TestCase):
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", tt.TEXT_TYPE_TEXT),
                TextNode("text", tt.TEXT_TYPE_BOLD),
                TextNode(" with an ", tt.TEXT_TYPE_TEXT),
                TextNode("italic", tt.TEXT_TYPE_ITALIC),
                TextNode(" word and a ", tt.TEXT_TYPE_TEXT),
                TextNode("code block", tt.TEXT_TYPE_CODE),
                TextNode(" and an ", tt.TEXT_TYPE_TEXT),
                TextNode(
                    "image", tt.TEXT_TYPE_IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and a ", tt.TEXT_TYPE_TEXT),
                TextNode("link", tt.TEXT_TYPE_LINK, "https://www.google.com"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
