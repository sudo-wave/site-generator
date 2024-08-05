import os

from generate_content import generate_page

# TODO: Edit the ./content/index.md file and remove the (sorry the link doesn't work yet) comment

# TODO: Create generate_pages_recursive(dir_path_content, template_path, dst_dir_path):
# 1. Crawl every entry in the {content} directory
# 2. For each markdown file found, generate a new {.html} file using the same {template.html}
# NOTE: The generated pages should be written to the {public} directory in the same directory structure


def generate_pages_recursive(content_path, template_path, dst_path):
    content_list = os.listdir(content_path)
    if len(content_list) >= 1:
        md_files = [file for file in content_list if file.endswith(".md")]
        for file in md_files:
            generate_page(file, template_path, dst_path)
        rest = [file for file in content_list if not file.endswith(".md")]
        for file in rest:
            if not os.path.isfile(file):
                new_content_path = os.path.join(content_path, file + "/")
                new_dst_path = os.path.join(dst_path, file + "/")
                os.mkdir(new_dst_path)
                generate_pages_recursive(new_content_path, template_path, new_dst_path)
