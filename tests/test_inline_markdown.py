import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
)
from textnode import (
    TEXT_TYPE_BOLD,
    TEXT_TYPE_CODE,
    TEXT_TYPE_IMAGE,
    TEXT_TYPE_ITALIC,
    TEXT_TYPE_LINK,
    TEXT_TYPE_TEXT,
    TextNode,
)


class TestSplitDelimiter(unittest.TestCase):
    def test_split_delimiter_return_list(self):
        node = TextNode("Text", TEXT_TYPE_TEXT)
        self.assertTrue(
            isinstance(split_nodes_delimiter([node], "*", TEXT_TYPE_TEXT), list)
        )

    def test_split_delimiter_text(self):
        node = TextNode("Regular text", TEXT_TYPE_TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "*", TEXT_TYPE_TEXT),
            [TextNode("Regular text", TEXT_TYPE_TEXT)],
        )

    def test_split_delimiter_bold(self):
        node = TextNode("This is text with a **bolded** word", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TEXT_TYPE_BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TEXT_TYPE_TEXT),
                TextNode("bolded", TEXT_TYPE_BOLD),
                TextNode(" word", TEXT_TYPE_TEXT),
            ],
            new_nodes,
        )

    def test_split_delimiter_code(self):
        node = TextNode("Text with a `code block` word", TEXT_TYPE_TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TEXT_TYPE_CODE),
            [
                TextNode("Text with a ", TEXT_TYPE_TEXT),
                TextNode("code block", TEXT_TYPE_CODE),
                TextNode(" word", TEXT_TYPE_TEXT),
            ],
        )

    def test_split_delimiter_italic(self):
        node = TextNode("Text with a *italicized* word", TEXT_TYPE_TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "*", TEXT_TYPE_ITALIC),
            [
                TextNode("Text with a ", TEXT_TYPE_TEXT),
                TextNode("italicized", TEXT_TYPE_ITALIC),
                TextNode(" word", TEXT_TYPE_TEXT),
            ],
        )

    def test_split_delimiter_image(self):
        node = TextNode("Text with a image", TEXT_TYPE_IMAGE)
        self.assertEqual(
            split_nodes_delimiter([node], "*", TEXT_TYPE_ITALIC),
            [TextNode("Text with a image", TEXT_TYPE_IMAGE)],
        )

    def test_split_delimiter_link(self):
        node = TextNode("Text with a link", TEXT_TYPE_LINK)
        self.assertEqual(
            split_nodes_delimiter([node], "*", TEXT_TYPE_ITALIC),
            [TextNode("Text with a link", TEXT_TYPE_LINK)],
        )

    def test_split_delimiter_double_bold(self):
        node = TextNode("One **bold** word and one more **bold** word", TEXT_TYPE_TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TEXT_TYPE_BOLD),
            [
                TextNode("One ", TEXT_TYPE_TEXT),
                TextNode("bold", TEXT_TYPE_BOLD),
                TextNode(" word and one more ", TEXT_TYPE_TEXT),
                TextNode("bold", TEXT_TYPE_BOLD),
                TextNode(" word", TEXT_TYPE_TEXT),
            ],
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**Bold** and *Italic*", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TEXT_TYPE_BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TEXT_TYPE_ITALIC)
        self.assertListEqual(
            [
                TextNode("Bold", TEXT_TYPE_BOLD),
                TextNode(" and ", TEXT_TYPE_TEXT),
                TextNode("Italic", TEXT_TYPE_ITALIC),
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
        node = TextNode("![image](https://i.imgur.com/zAV93b)", TEXT_TYPE_TEXT)
        self.assertEqual(
            split_nodes_images([node]),
            [TextNode("image", TEXT_TYPE_IMAGE, "https://i.imgur.com/zAV93b")],
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is a ![image](https://i.imgur.com/zAV93b)", TEXT_TYPE_TEXT
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode("This is a ", TEXT_TYPE_TEXT),
                TextNode("image", TEXT_TYPE_IMAGE, "https://i.imgur.com/zAV93b"),
            ],
        )

    def test_split_nodes_images(self):
        node = TextNode(
            "This is a ![cat image](https://imgur.com/cat.png) and a ![dog gif](https://imgur.com/dog.gif)!",
            TEXT_TYPE_TEXT,
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode("This is a ", TEXT_TYPE_TEXT),
                TextNode("cat image", TEXT_TYPE_IMAGE, "https://imgur.com/cat.png"),
                TextNode(" and a ", TEXT_TYPE_TEXT),
                TextNode("dog gif", TEXT_TYPE_IMAGE, "https://imgur.com/dog.gif"),
                TextNode("!", TEXT_TYPE_TEXT),
            ],
        )


class TestSplitLinks(unittest.TestCase):
    def test_split_nodes_single_link(self):
        node = TextNode("[link](https://www.google.com)", TEXT_TYPE_TEXT)
        self.assertEqual(
            split_nodes_links([node]),
            [TextNode("link", TEXT_TYPE_LINK, "https://www.google.com")],
        )

    def test_split_nodes_link(self):
        node = TextNode("This is a [link](https://www.netflix.com)", TEXT_TYPE_TEXT)
        self.assertEqual(
            split_nodes_links([node]),
            [
                TextNode("This is a ", TEXT_TYPE_TEXT),
                TextNode("link", TEXT_TYPE_LINK, "https://www.netflix.com"),
            ],
        )

    def test_split_nodes_links(self):
        node = TextNode(
            "This is a [link](https://www.amazon.com) and a [another link](https://www.pinterest.com)",
            TEXT_TYPE_TEXT,
        )
        self.assertEqual(
            split_nodes_links([node]),
            [
                TextNode("This is a ", TEXT_TYPE_TEXT),
                TextNode("link", TEXT_TYPE_LINK, "https://www.amazon.com"),
                TextNode(" and a ", TEXT_TYPE_TEXT),
                TextNode("another link", TEXT_TYPE_LINK, "https://www.pinterest.com"),
            ],
        )


class TestTextToNode(unittest.TestCase):
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TEXT_TYPE_TEXT),
                TextNode("text", TEXT_TYPE_BOLD),
                TextNode(" with an ", TEXT_TYPE_TEXT),
                TextNode("italic", TEXT_TYPE_ITALIC),
                TextNode(" word and a ", TEXT_TYPE_TEXT),
                TextNode("code block", TEXT_TYPE_CODE),
                TextNode(" and an ", TEXT_TYPE_TEXT),
                TextNode("image", TEXT_TYPE_IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TEXT_TYPE_TEXT),
                TextNode("link", TEXT_TYPE_LINK, "https://www.google.com"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
