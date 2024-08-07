class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError(".to_html() method not implemented")

    def props_to_html(self):
        """Return a string that represents the HTML attributes of the node.

        >>> node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        >>> print(node.props_to_html())
         href="https://www.google.com" target="_blank"
        """
        html_attributes = ""
        if self.props is None:
            return html_attributes
        for prop in self.props:
            html_attributes += f' {prop}="{self.props.get(prop)}"'
        return html_attributes

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        """Renders a leaf node as an HTML string (by returning a string).

        >>> node = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        >>> print(node.to_html())
        <a href="https://www.google.com">Click me!</a>
        """
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        """Return a string representation of the HTML tag and node and its children.

        >>> node = ParentNode("p", [LeafNode(None, "Normal Text"), LeafNode("b", "Bold Text"), LeafNode(None, "Normal Text")])
        >>> print(node.to_html())
        <p>Normal Text<b>Bold Text</b>Normal Text</p>
        """
        if self.tag is None:
            raise ValueError("Invalid HTML: does not contain tag")
        if self.children is None:
            raise ValueError("Invalid HTML: does not contain children")
        html_string = "<" + self.tag + self.props_to_html() + ">"
        if isinstance(self, LeafNode):
            return self.props_to_html()
        if len(self.children) == 0:
            return html_string + "</" + self.tag + ">"
        for child in self.children:
            html_string += child.to_html()
        return html_string + "</" + self.tag + ">"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
