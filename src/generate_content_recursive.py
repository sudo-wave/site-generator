import os

from generate_content import generate_page


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
