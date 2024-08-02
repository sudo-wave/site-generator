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
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)


class TestSplitDelimiter(unittest.TestCase):
    def test_split_delimiter_return_list(self):
        node = TextNode("Text", text_type_text)
        self.assertTrue(
            isinstance(split_nodes_delimiter([node], "*", text_type_text), list)
        )

    def test_split_delimiter_text(self):
        node = TextNode("Regular text", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "*", text_type_text),
            [TextNode("Regular text", text_type_text)],
        )

    def test_split_delimiter_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_split_delimiter_code(self):
        node = TextNode("Text with a `code block` word", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "`", text_type_code),
            [
                TextNode("Text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
        )

    def test_split_delimiter_italic(self):
        node = TextNode("Text with a *italicized* word", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "*", text_type_italic),
            [
                TextNode("Text with a ", text_type_text),
                TextNode("italicized", text_type_italic),
                TextNode(" word", text_type_text),
            ],
        )

    def test_split_delimiter_image(self):
        node = TextNode("Text with a image", text_type_image)
        self.assertEqual(
            split_nodes_delimiter([node], "*", text_type_italic),
            [TextNode("Text with a image", text_type_image)],
        )

    def test_split_delimiter_link(self):
        node = TextNode("Text with a link", text_type_link)
        self.assertEqual(
            split_nodes_delimiter([node], "*", text_type_italic),
            [TextNode("Text with a link", text_type_link)],
        )

    def test_split_delimiter_double_bold(self):
        node = TextNode("One **bold** word and one more **bold** word", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "**", text_type_bold),
            [
                TextNode("One ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word and one more ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word", text_type_text),
            ],
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**Bold** and *Italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("Bold", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("Italic", text_type_italic),
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
        node = TextNode("![image](https://i.imgur.com/zAV93b)", text_type_text)
        self.assertEqual(
            split_nodes_images([node]),
            [TextNode("image", text_type_image, "https://i.imgur.com/zAV93b")],
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is a ![image](https://i.imgur.com/zAV93b)", text_type_text
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode("This is a ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zAV93b"),
            ],
        )

    def test_split_nodes_images(self):
        node = TextNode(
            "This is a ![cat image](https://imgur.com/cat.png) and a ![dog gif](https://imgur.com/dog.gif)!",
            text_type_text,
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode("This is a ", text_type_text),
                TextNode("cat image", text_type_image, "https://imgur.com/cat.png"),
                TextNode(" and a ", text_type_text),
                TextNode("dog gif", text_type_image, "https://imgur.com/dog.gif"),
                TextNode("!", text_type_text),
            ],
        )


class TestSplitLinks(unittest.TestCase):
    def test_split_nodes_single_link(self):
        node = TextNode("[link](https://www.google.com)", text_type_text)
        self.assertEqual(
            split_nodes_links([node]),
            [TextNode("link", text_type_link, "https://www.google.com")],
        )

    def test_split_nodes_link(self):
        node = TextNode("This is a [link](https://www.netflix.com)", text_type_text)
        self.assertEqual(
            split_nodes_links([node]),
            [
                TextNode("This is a ", text_type_text),
                TextNode("link", text_type_link, "https://www.netflix.com"),
            ],
        )

    def test_split_nodes_links(self):
        node = TextNode(
            "This is a [link](https://www.amazon.com) and a [another link](https://www.pinterest.com)",
            text_type_text,
        )
        self.assertEqual(
            split_nodes_links([node]),
            [
                TextNode("This is a ", text_type_text),
                TextNode("link", text_type_link, "https://www.amazon.com"),
                TextNode(" and a ", text_type_text),
                TextNode("another link", text_type_link, "https://www.pinterest.com"),
            ],
        )


class TestTextToNode(unittest.TestCase):
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://www.google.com"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
