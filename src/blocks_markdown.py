import os

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

tag_paragraph = "p"
tag_pretext = "pre"
tag_code = "code"
tag_quote = "blockquote"
tag_list_item = "li"
tag_unordered_list = "ul"
tag_ordered_list = "ol"

CWD = os.getcwd()
DIR = os.listdir(CWD)
CWD += "/testfiles"


def get_markdown_file():
    markdown_file = input("Enter filename: ")
    file_directory = CWD + f"/{markdown_file}"
    if os.path.exists(file_directory):
        return file_directory


def read_markdown_file(markdown_file):
    if markdown_file is None:
        raise Exception("File does not exist")
    with open(markdown_file, "r") as file:
        lines = file.readlines()
    return lines


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = [block.strip() for block in blocks if block != ""]
    return filtered_blocks


# Previous code for function above
#    markdown_block = []
#    text = ""
#    for line in markdown:
#        if line != "\n":
#            line = line.strip()
#            text += line
#        else:
#            markdown_block.append(text)
#            text = ""
#    if text != "":
#        markdown_block.append(text)
#    return markdown_block


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
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if markdown_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if markdown_block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_unordered_list
    if markdown_block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_unordered_list
    if markdown_block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_ordered_list
    return block_type_paragraph


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
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    if block_type == block_type_unordered_list:
        return unordered_list_to_html_node(block)
    if block_type == block_type_ordered_list:
        return ordered_list_to_html_node(block)


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode(tag_paragraph, children)


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
    code_node = ParentNode(tag_code, children)
    return ParentNode(tag_pretext, [code_node])


def quote_to_html_node(block):
    new_lines = []
    lines = block.split("\n")
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode(tag_quote, children)


def unordered_list_to_html_node(block):
    node_items = []
    items = block.split("\n")
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        node_items.append(ParentNode(tag_list_item, children))
    return ParentNode(tag_unordered_list, node_items)


def ordered_list_to_html_node(block):
    node_items = []
    items = block.split("\n")
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        node_items.append(ParentNode(tag_list_item, children))
    return ParentNode(tag_ordered_list, node_items)
