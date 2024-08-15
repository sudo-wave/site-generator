"""A module for representing and manipulating a simple HTML document object model (DOM) tree."""


class HTMLNode:
    """A class to represent an HTML node in a document object model (DOM) tree.

    Attributes:
    tag: str, optional
        The HTML tag (e.g., 'div', 'p', 'a') associated with this node.
        Default is None.
    value: str, optional
        The text content or value associated with this node.
        Default is None.
    children: list of HTMLNode, optional
        A list of child nodes representing the nested structure within this node.
        Default is None.
    props: dict, optional
        A dictionary of properties/attributes (e.g., {'id': 'main', 'class': 'container'}).
        Default is None.
    """

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """Convert the HTMLNode object and its children into an HTML string representation

        Raises: NotImplementedError
            Method not implemented in HTMLNode class
        """
        raise NotImplementedError(".to_html() method not implemented")

    def props_to_html(self):
        """Convert the properties of the HTMLNode instance into a string of HTML attributes

        Returns:
        str
            HTML attributes represented as a string, formatted  as key-value pairs
            If the 'props' attribute is None an empty string is returned
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
    """A class to represent a leaf node in the DOM tree (does not have any child nodes).
    Inherits from the HTMLNode class.

    Attributes:
    tag: str
        The HTML tag name (e.g., 'img', 'input') associated with this leaf node.
    value: str
        The text content or value associated with this leaf node.
    props: dict, optional
        A dictionary of properties/attributes (e.g., {'src': 'image.png'}).
        Default is None.
    """

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        """Convert the LeafNode  instance into an HTML string representation.

        Returns: str
            The HTML string representing this leaf node, including its tag, attributes, and value.
        """
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    """A class to represent a parent node in the DOM tree.
    Can have one or more child nodes.
    Inherits from the HTMLNode class.

    Attributes:
    tag: str
        The HTML tag name (e.g., 'div', 'ul') associated with this parent node.
    children: list of HTMLNode
        A list of child nodes representing the nested structure within this parent node.
    props: dict, optional
        A dictionary of properties/attributes (e.g., {'id': 'container', 'class': 'main'}).
        Default is None.
    """

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        """Convert the ParentNode into an HTML string representation.

        Returns: str
        HTML string representing this node, including its tag, attributes, and HTML of its children.

        Raises: ValueError
        If the node has no tag (i.e., 'self.tag' is None) or if the node has no
        children (i.e., 'self.children' is None).

        Notes:
        For a 'LeafNode', the method returns the properties as an HTML attribute string.
        If the node has no children, the method returns a self-closing tag.
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
