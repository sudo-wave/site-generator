import os
import shutil

path_static = "./static/"
path_public = "./public/"


def main():
    # First delete the contents of the public path
    path_public_list = os.listdir(path_public)
    delete_contents(path_public_list)
    # Copy the contents of the of the static path
    # into the empty public path
    path_static_list = os.listdir(path_static)
    copy_contents(path_static_list, path_static, path_public)


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


main()
