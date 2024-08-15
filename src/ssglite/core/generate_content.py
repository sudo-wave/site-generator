import os
from parser import markdown_to_html_node


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


def generate_pages_recursive(content_path, template_path, dst_path):
    content_list = os.listdir(content_path)
    if len(content_list) >= 1:
        md_files = [file for file in content_list if file.endswith(".md")]
        for file in md_files:
            file_path = os.path.join(content_path, file)
            generate_page(file_path, template_path, dst_path)
        rest = [file for file in content_list if not file.endswith(".md")]
        for file in rest:
            if not os.path.isfile(file):
                new_content_path = os.path.join(content_path, file + "/")
                new_dst_path = os.path.join(dst_path, file + "/")
                os.mkdir(new_dst_path)
                generate_pages_recursive(new_content_path, template_path, new_dst_path)
