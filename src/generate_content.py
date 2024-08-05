import os

from blocks_markdown import markdown_to_html_node


def extract_title(markdown):
    markdown = markdown.strip()
    header = ""
    for line in markdown:
        if line == "\n":
            break
        header += line
    if not header.startswith("# "):
        raise Exception("Markdown file does not contain an <h1> header")
    lines = header.replace("#", "").strip()
    return lines


def generate_page(from_path, template_path, dst_path):
    print(f"Generating webpage from {from_path} to {dst_path} using {template_path}")
    markdown = template = ""
    with open(from_path, "r") as markdown_file:
        for line in markdown_file:
            markdown += line
    with open(template_path, "r") as template_file:
        for line in template_file:
            template += line
    html_string = markdown_to_html_node(markdown).to_html()
    title_page = extract_title(markdown)
    template = template.replace("{{ Title }}", title_page).replace(
        "{{ Content }}", html_string
    )
    html_index = "index.html"
    path_final = os.path.join(dst_path, html_index)
    with open(path_final, "w") as file:
        file.write(template)


extract_title(
    """
# This is a title

# This is a second title that should be ignored
"""
)
