import re

from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)

bold_delimiter = "**"
code_delimiter = "`"
italic_delimiter = "*"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Return a list of nodes where any 'text' type nodes are potentially
    split into multiple nodes based on syntax

    >>> node = TextNode("This is text with a **bolded** word in the middle", "text")
    >>> split_nodes_delimiter([node], "**", text_type_bold)
    [TextNode(This is text with a , text, None), TextNode(bolded, bold, None), TextNode( word in the middle, text, None)]
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    match = re.findall(pattern, text)
    return match


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    match = re.findall(pattern, text)
    return match


def split_nodes_images(old_nodes):
    """Return a list of nodes where any of the old nodes are split into
    distinct nodes respective to text type

    >>> node = TextNode("This is a ![image](https://imgur.com/cat.jpeg)", "text")
    >>> split_nodes_images([node])
    [TextNode(This is a , text, None), TextNode(image, image, https://imgur.com/cat.jpeg)]
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        text_copy = node.text
        images = extract_markdown_images(text_copy)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            image_alt, image_url = image[0], image[1]
            sections = text_copy.split(f"![{image_alt}]({image_url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid Markdown format: image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(image_alt, text_type_image, image_url))
            text_copy = sections[1]
        if text_copy != "":
            new_nodes.append(TextNode(text_copy, text_type_text))
    return new_nodes


def split_nodes_links(old_nodes):
    """Return a list of nodes where any of the old nodes are split into
    distinct nodes respective to text type

    >>> node = TextNode("This is a ![link](https://www.hulu.com)", "text")
    >>> split_nodes_links([node])
    [TextNode(This is a , text, None), TextNode(link, link, https://www.hulu.com)]
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        text_copy = node.text
        links = extract_markdown_links(text_copy)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            link_alt, link_url = link[0], link[1]
            sections = text_copy.split(f"[{link_alt}]({link_url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid Markdown format: link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link_alt, text_type_link, link_url))
            text_copy = sections[1]
        if text_copy != "":
            new_nodes.append(TextNode(text_copy, text_type_text))
    return new_nodes


def text_to_textnodes(text):
    node = [TextNode(text, text_type_text)]
    node = split_nodes_delimiter(node, bold_delimiter, text_type_bold)
    node = split_nodes_delimiter(node, code_delimiter, text_type_code)
    node = split_nodes_delimiter(node, italic_delimiter, text_type_italic)
    node = split_nodes_images(node)
    node = split_nodes_links(node)
    return node


if __name__ == "__main__":
    import doctest

    doctest.testmod()
