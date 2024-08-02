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
