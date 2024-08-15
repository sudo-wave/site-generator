import constants
from nodes import ParentNode, text_node_to_html_node

from .inline_markdown import text_to_textnodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = [block.strip() for block in blocks if block != ""]
    return filtered_blocks


def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")

    if (
        markdown_block.startswith("# ")
        or markdown_block.startswith("## ")
        or markdown_block.startswith("### ")
        or markdown_block.startswith("#### ")
        or markdown_block.startswith("##### ")
        or markdown_block.startswith("###### ")
    ):
        return constants.BLOCK_TYPE_HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return constants.BLOCK_TYPE_CODE
    if markdown_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return constants.BLOCK_TYPE_PARAGRAPH
        return constants.BLOCK_TYPE_QUOTE
    if markdown_block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return constants.BLOCK_TYPE_PARAGRAPH
        return constants.BLOCK_TYPE_UNORDERED_LIST
    if markdown_block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return constants.BLOCK_TYPE_PARAGRAPH
        return constants.BLOCK_TYPE_UNORDERED_LIST
    if markdown_block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return constants.BLOCK_TYPE_PARAGRAPH
            i += 1
        return constants.BLOCK_TYPE_ORDERED_LIST
    return constants.BLOCK_TYPE_PARAGRAPH


def markdown_to_html_node(markdown):
    children = []
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        child_node = create_child_node(block)
        children.append(child_node)
    parent_node = ParentNode("div", children)
    return parent_node


def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        child_node = text_node_to_html_node(node)
        children.append(child_node)
    return children


def create_child_node(block):
    block_type = block_to_block_type(block)
    if block_type == constants.BLOCK_TYPE_PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == constants.BLOCK_TYPE_HEADING:
        return heading_to_html_node(block)
    if block_type == constants.BLOCK_TYPE_CODE:
        return code_to_html_node(block)
    if block_type == constants.BLOCK_TYPE_QUOTE:
        return quote_to_html_node(block)
    if block_type == constants.BLOCK_TYPE_UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == constants.BLOCK_TYPE_ORDERED_LIST:
        return ordered_list_to_html_node(block)


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode(constants.TAG_PARAGRAPH, children)


def heading_to_html_node(block):
    num = 0
    for b in block:
        if b == "#":
            num += 1
        else:
            break
    if num + 1 >= len(block):
        raise ValueError(f"Invalid header level: {num}")
    text = block[num + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{num}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code_node = ParentNode(constants.TAG_CODE, children)
    return ParentNode(constants.TAG_PRETEXT, [code_node])


def quote_to_html_node(block):
    new_lines = []
    lines = block.split("\n")
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode(constants.TAG_QUOTE, children)


def unordered_list_to_html_node(block):
    node_items = []
    items = block.split("\n")
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        node_items.append(ParentNode(constants.TAG_LIST_ITEM, children))
    return ParentNode(constants.TAG_UNORDERED_LIST, node_items)


def ordered_list_to_html_node(block):
    node_items = []
    items = block.split("\n")
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        node_items.append(ParentNode(constants.TAG_LIST_ITEM, children))
    return ParentNode(constants.TAG_ORDERED_LIST, node_items)
