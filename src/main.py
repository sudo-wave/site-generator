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
