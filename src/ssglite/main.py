import os

from core import copy_contents, delete_contents, generate_pages_recursive

path_static = "./static/"
path_public = "./public/"
path_content = "./content/"
path_template = "template.html"


def main():
    # First delete the ./public/ folder
    delete_contents(path_public)
    # Copy the contents of the of the static path into ./public/
    path_static_list = os.listdir(path_static)
    copy_contents(path_static, path_static_list, path_public)
    # After copying, generate a new index.html in ./public from ./content
    generate_pages_recursive(path_content, path_template, path_public)


main()
