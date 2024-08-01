class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        """Return a string that represents the HTML attributes of the node.

        >>> prop = {"href": "https://www.google.com", "target": "_blank"}
        >>> node = HTMLNode(props=prop)
        >>> print(node.props_to_html())
         href="https://www.google.com" target="_blank"
        """
        html_attributes = ""
        if self.props == None:
            return html_attributes
        for i in self.props:
            html_attributes = html_attributes + f' {i}="{self.props.get(i)}"'
        return html_attributes

    def __repr__(self):
        return (
            "HTMLNode(\n"
            f"  tag={self.tag}\n"
            f"  value={self.value}\n"
            f"  children={self.children}\n"
            f"  props={self.props_to_html()}\n"
            ")"
        )


class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")

    def to_html(self):
        """Renders a leaf node as an HTML string (by returning a string).

        >>> node1 = LeafNode(tag="p", value="This is a paragraph of text.", props=None)
        >>> print(node1.to_html())
        <p>This is a paragraph of text.</p>
        >>> node2 = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        >>> print(node2.to_html())
        <a href="https://www.google.com">Click me!</a>
        """
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
