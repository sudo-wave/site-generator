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


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type:
            new_nodes.append(node)
            continue
        split = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid Markdown format, section is not closed")
        for n in range(len(sections)):
            if sections[n] == "":
                continue
            if n % 2 == 0:
                split.append(TextNode(sections[n], text_type_text))
            else:
                split.append(TextNode(sections[n], text_type))
        new_nodes.extend(split)
    return new_nodes


def split_nodes_images(old_nodes):
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
                raise ValueError("Invalid Markdown format, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(image_alt, text_type_image, image_url))
            text_copy = sections[1]
        if text_copy != "":
            new_nodes.append(TextNode(text_copy, text_type_text))
    return new_nodes


def split_nodes_links(old_nodes):
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
            sections = text_copy.split(f"![{link_alt}]({link_url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid Markdown format, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link_alt, text_type_link, link_url))
            text_copy = sections[1]
        if text_copy != "":
            new_nodes.append(TextNode(text_copy, text_type_text))
    return new_nodes


def text_to_textnodes(text):
    return split_nodes_images(
        split_nodes_links(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [TextNode(text, text_type_text)], bold_delimiter, text_type_bold
                    ),
                    code_delimiter,
                    text_type_code,
                ),
                italic_delimiter,
                text_type_italic,
            )
        )
    )
