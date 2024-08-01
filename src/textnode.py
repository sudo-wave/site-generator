class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        """Returns True if all of the properties of two TextNode objects are equal.

        >>> text1 = "node"
        >>> text2 = "not a node"
        >>> text_type1 = "normal"
        >>> text_type2 = "not normal"
        >>> n1 = TextNode(text1, text_type1)
        >>> n2 = TextNode(text1, text_type1)
        >>> n1 == n2
        True
        >>> n3 = TextNode(text1, text_type1)
        >>> n4 = TextNode(text2, text_type1)
        >>> n3 == n4
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

        >>> n1 = TextNode("node1", "normal", "123")
        >>> n2 = TextNode("node2", "bold", "abc")
        >>> n3 = TextNode("node3", "italic")
        >>> n4 = TextNode("node4", "normal", "https://google.com")
        >>> print(n1)
        TextNode(node1, normal, 123)
        >>> print(n2)
        TextNode(node2, bold, abc)
        >>> print(n3)
        TextNode(node3, italic, None)
        >>> print(n4)
        TextNode(node4, normal, https://google.com)
        """
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
