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

        >>> n1 = TextNode("Node", "text")
        >>> n2 = TextNode("Node", "text")
        >>> n3 = TextNode("Node", "bold")
        >>> n1 == n2
        True
        >>> n1 == n3
        False
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

        >>> n1 = TextNode("node1", "text", "123")
        >>> n2 = TextNode("node2", "bold", "abc")
        >>> print(n1)
        TextNode(node1, text, 123)
        >>> print(n2)
        TextNode(node2, bold, abc)
        """
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
