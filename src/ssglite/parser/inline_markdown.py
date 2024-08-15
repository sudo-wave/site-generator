"""Random"""

import re

import ssglite.constants as tt
from ssglite.nodes import TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Return a list of nodes where any 'text' type nodes are potentially
    split into multiple nodes based on syntax
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != tt.TEXT_TYPE_TEXT:
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
                split_nodes.append(TextNode(sections[i], tt.TEXT_TYPE_TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    """Return a match if an images is found"""
    pattern = r"!\[(.*?)\]\((.*?)\)"
    match = re.findall(pattern, text)
    return match


def extract_markdown_links(text):
    """Return a match if a link is found"""
    pattern = r"\[(.*?)\]\((.*?)\)"
    match = re.findall(pattern, text)
    return match


def split_nodes_images(old_nodes):
    """Return a list of nodes where any of the old nodes are split into
    distinct nodes respective to text type
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != tt.TEXT_TYPE_TEXT:
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
                new_nodes.append(TextNode(sections[0], tt.TEXT_TYPE_TEXT))
            new_nodes.append(TextNode(image_alt, tt.TEXT_TYPE_IMAGE, image_url))
            text_copy = sections[1]
        if text_copy != "":
            new_nodes.append(TextNode(text_copy, tt.TEXT_TYPE_TEXT))
    return new_nodes


def split_nodes_links(old_nodes):
    """Return a list of nodes where any of the old nodes are split into
    distinct nodes respective to text type
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != tt.TEXT_TYPE_TEXT:
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
                new_nodes.append(TextNode(sections[0], tt.TEXT_TYPE_TEXT))
            new_nodes.append(TextNode(link_alt, tt.TEXT_TYPE_LINK, link_url))
            text_copy = sections[1]
        if text_copy != "":
            new_nodes.append(TextNode(text_copy, tt.TEXT_TYPE_TEXT))
    return new_nodes


def text_to_textnodes(text):
    """Returns a TextNode based on the input text"""
    node = [TextNode(text, tt.TEXT_TYPE_TEXT)]
    node = split_nodes_delimiter(node, tt.DELIMITER_BOLD, tt.TEXT_TYPE_BOLD)
    node = split_nodes_delimiter(node, tt.DELIMITER_CODE, tt.TEXT_TYPE_CODE)
    node = split_nodes_delimiter(node, tt.DELIMITER_ITALIC, tt.TEXT_TYPE_ITALIC)
    node = split_nodes_images(node)
    node = split_nodes_links(node)
    return node
