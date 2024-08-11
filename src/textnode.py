"""Module providing a LeafNode object"""

from htmlnode import LeafNode

TEXT_TYPE_TEXT = "text"
TEXT_TYPE_BOLD = "bold"
TEXT_TYPE_ITALIC = "italic"
TEXT_TYPE_CODE = "code"
TEXT_TYPE_LINK = "link"
TEXT_TYPE_IMAGE = "image"


class TextNode:
    """Class representing a html text node"""

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        """Returns True if all the properties of two TextNode objects are equal

        >>> node1 = TextNode("Node", "text")
        >>> node2 = TextNode("Node", "text")
        >>> node1 == node2
        True
        """
        if self.text != other.text:
            return False
        if self.text_type != other.text_type:
            return False
        if self.url != other.url:
            return False
        return True

    def __repr__(self):
        """Returns representation of a TextNode object e.g.,

        >>> node = TextNode("Text goes here", "Text type", "URL")
        >>> print(node)
        TextNode(Text goes here, Text type, URL)
        """
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    """Return the respective LeafNode conversion from given TextNode

    >>> node = TextNode("Random text on one line.", TEXT_TYPE_BOLD)
    >>> text_node_to_html_node(node)
    LeafNode(b, Random text on one line., None)
    """
    node_text_type = text_node.text_type
    node_text = text_node.text
    if node_text_type == TEXT_TYPE_BOLD:
        return LeafNode("b", node_text)
    if node_text_type == TEXT_TYPE_CODE:
        return LeafNode("code", node_text)
    if node_text_type == TEXT_TYPE_IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": node_text})
    if node_text_type == TEXT_TYPE_ITALIC:
        return LeafNode("i", node_text)
    if node_text_type == TEXT_TYPE_LINK:
        return LeafNode("a", node_text, {"href": text_node.url})
    if node_text_type == TEXT_TYPE_TEXT:
        return LeafNode(None, node_text)
    raise ValueError(f"Invalid text type, {node_text_type}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
