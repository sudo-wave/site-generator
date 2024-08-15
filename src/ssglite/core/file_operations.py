import os
import shutil


def delete_contents(public_path):
    # If the public path exists, delete the folder
    # and all of its contents.
    if os.path.exists(public_path):
        print("Deleting ./public/ folder")
        shutil.rmtree(public_path)


def copy_contents(src_path, src_path_arr, dst_path):
    if not os.path.exists(dst_path):
        print("Recreating ./public/ folder")
        os.mkdir(dst_path)
        print("Copying contents from ./static/ to ./public/")

    if len(src_path_arr) >= 1:
        curr_path = os.path.join(src_path, src_path_arr[0])
        # If the first item in the current source path is a file,
        # copy the contents of the file into the destination path.
        # ex: ../static/index.css -> COPY index.css -> ../public/index.css
        if os.path.isfile(curr_path):
            shutil.copy(curr_path, dst_path)
        # If the first item is a folder, create the directory in the
        # destination path. Afterwards we call copy_contents inside
        # of the folder
        # ex: ../static/images/ -> COPY images -> ../public/images/
        # -> CALL COPY_CONTENTS -> ../static/images/rivendell.png -> COPY rivendell.png
        # -> ../public/images/
        else:
            curr_path += "/"
            new_src_path_arr = os.listdir(curr_path)
            new_dst_path = os.path.join(dst_path, src_path_arr[0] + "/")
            os.mkdir(new_dst_path)
            copy_contents(curr_path, new_src_path_arr, new_dst_path)
        copy_contents(src_path, src_path_arr[1:], dst_path)
