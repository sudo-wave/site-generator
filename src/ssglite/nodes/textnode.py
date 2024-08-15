"""Module providing a LeafNode object"""

import constants

from .htmlnode import LeafNode


class TextNode:
    """Class representing a html text node"""

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        """Returns True if all the properties of two TextNode objects are equal"""
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        return True

    def __repr__(self):
        """Returns representation of a TextNode object e.g.,"""
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    """Return the respective LeafNode conversion from given TextNode"""
    node_text_type = text_node.text_type
    node_text = text_node.text
    if node_text_type == constants.TEXT_TYPE_BOLD:
        return LeafNode("b", node_text)
    if node_text_type == constants.TEXT_TYPE_CODE:
        return LeafNode("code", node_text)
    if node_text_type == constants.TEXT_TYPE_IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": node_text})
    if node_text_type == constants.TEXT_TYPE_ITALIC:
        return LeafNode("i", node_text)
    if node_text_type == constants.TEXT_TYPE_LINK:
        return LeafNode("a", node_text, {"href": text_node.url})
    if node_text_type == constants.TEXT_TYPE_TEXT:
        return LeafNode(None, node_text)
    raise ValueError(f"Invalid text type, {node_text_type}")
