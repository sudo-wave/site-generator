from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        """Returns True if all of the properties of two TextNode objects are equal.

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
        """Returns a string representation of the TextNode object, i.e.,
        TextNode(text, text_type, url)

        >>> node = TextNode("Text goes here", "Text type", "URL")
        >>> print(node)
        TextNode(Text goes here, Text type, URL)
        """
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    """Return the respective LeafNode conversion from given TextNode

    >>> node = TextNode("Random text on one line.", text_type_bold)
    >>> text_node_to_html_node(node)
    LeafNode(b, Random text on one line., None)
    """
    node_text_type = text_node.text_type
    node_text = text_node.text
    if node_text_type == text_type_bold:
        return LeafNode("b", node_text)
    if node_text_type == text_type_code:
        return LeafNode("code", node_text)
    if node_text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": node_text})
    if node_text_type == text_type_italic:
        return LeafNode("i", node_text)
    if node_text_type == text_type_link:
        return LeafNode("a", node_text, {"href": text_node.url})
    if node_text_type == text_type_text:
        return LeafNode(None, node_text)
    raise Exception(f"Invalid text type, {node_text_type}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
