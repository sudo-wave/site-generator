import re

from htmlnode import *
from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)


def text_node_to_html_node(text_node):
    text = text_node.get_text()
    text_type = text_node.get_text_type()
    if text_type == text_type_bold:
        return LeafNode("b", text)
    elif text_type == text_type_code:
        return LeafNode("code", text)
    elif text_type == text_type_image and text_node.get_url() is not None:
        return LeafNode("img", "", {"src": text_node.get_url(), "alt": text})
    elif text_type == text_type_image and text_node.get_url() is None:
        raise Exception("Invalid URL")
    elif text_type == text_type_italic:
        return LeafNode("i", text)
    elif text_type == text_type_link and text_node.get_url() is not None:
        return LeafNode("a", text, {"href": text_node.get_url()})
    elif text_type == text_type_link and text_node.get_url() is None:
        raise Exception("Invalid URL")
    elif text_type == text_type_text:
        return LeafNode(None, text)
    else:
        raise Exception("Invalid text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        node_text_type = node.get_text_type()
        node_text = node.get_text()
        if node_text_type == text_type_text:
            if node_text.count(delimiter) == 0:
                new_nodes.extend([TextNode(node_text, node_text_type)])
                break
            if node_text.count(delimiter) != 2:
                raise Exception(f"Invalid Markdown syntax: missing {delimiter}")
            text_lst = node_text.split(delimiter)
            for idx in range(len(text_lst)):
                if idx == 1:
                    new_nodes.extend([TextNode(text_lst[idx], text_type)])
                else:
                    new_nodes.extend([TextNode(text_lst[idx], node_text_type)])
        else:
            new_nodes.extend([TextNode(node_text, node_text_type)])
    return new_nodes


def check_text_type(text_type, text_types):
    return text_type in text_types


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_text = node.get_text()
        images = extract_markdown_images(node_text)
        if len(images) != 2:
            new_nodes.extend([node])
            continue
        if len(node_text) == 0:
            continue
        text_copy = node_text
        for image in images:
            image_alt, image_url = image[0], image[1]
            text_split = text_copy.split(f"![{image_alt}]({image_url})")
            if len(text_split[0]) != 0:
                new_nodes.extend([TextNode(text_split[0], text_type_text)])
            new_nodes.extend([TextNode(image_alt, text_type_image, image_url)])
            text_copy = "".join(text_split[1:])
        if len(text_copy) != 0:
            new_nodes.extend([TextNode(text_copy[0], text_type_text)])
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_text = node.get_text()
        links = extract_markdown_links(node_text)
        if len(links) != 2:
            new_nodes.extend([node])
            continue
        if len(node_text) == 0:
            continue
        text_copy = node_text
        for link in links:
            link_alt, link_url = link[0], link[1]
            text_split = text_copy.split(f"![{link_alt}]({link_url})")
            if len(text_split[0]) != 0:
                new_nodes.extend([TextNode(text_split[0], text_type_text)])
            new_nodes.extend([TextNode(link_alt, text_type_link, link_url)])
            text_copy = "".join(text_split[1:])
        if len(text_copy) != 0:
            new_nodes.extend([TextNode(text_copy[0], text_type_text)])
    return new_nodes
