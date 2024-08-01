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
        if self.props == None:
            return None
        html_attributes = ""
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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
