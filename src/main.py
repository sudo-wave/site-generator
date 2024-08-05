import os
import shutil

from blocks_markdown import markdown_to_html_node

path_static = "./static/"
path_public = "./public/"
path_content = "./content/"
path_template = "template.html"


def main():
    # First delete the contents of the public path
    path_public_list = os.listdir(path_public)
    delete_contents(path_public_list)
    # Copy the contents of the of the static path
    # into the empty public path
    path_static_list = os.listdir(path_static)
    copy_contents(path_static_list, path_static, path_public)
    generate_page(path_content + "index.md", path_template, path_public)


def delete_contents(path_arr):
    if len(path_arr) >= 1:
        path = path_public + path_arr[0]
        # If the path is a file, the file is removed from the path
        # ex: ../public/text.txt -> REMOVE text.txt -> ../public/
        if os.path.isfile(path):
            os.remove(path)
        # If the path is a directory, the file is removed from the path
        # ex: ../public/example/ -> REMOVE example/ -> ../public/
        else:
            shutil.rmtree(path + "/")
        delete_contents(path_arr[1:])


def copy_contents(path_arr, path_src, path_dst):
    if len(path_arr) >= 1:
        path_src_curr = path_src + path_arr[0]
        # If the source path is a file it is copied into the
        # non updated destination path.
        # ex: ../static/index.css -> COPY index.css -> ../public/index.css
        if os.path.isfile(path_src_curr):
            shutil.copy(path_src_curr, path_dst)
        # If the source path is a directory, the directory is
        # copied into the destination path and copy_contents is called
        # from the source path.
        # ex: ../static/images/ -> COPY images -> ../public/images/
        # -> CALL COPY_CONTENTS -> ../static/images/rivendell.png -> COPY rivendell.png
        # -> ../public/images/
        else:
            os.mkdir(path_dst + path_arr[0] + "/")
            path_arr_new = os.listdir(path_src_curr + "/")
            copy_contents(
                path_arr_new, path_src_curr + "/", path_dst + path_arr[0] + "/"
            )
        copy_contents(path_arr[1:], path_src, path_dst)


def extract_title(markdown):
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
    return None


main()
