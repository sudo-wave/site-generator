import os
import shutil


def delete_contents(public_path):
    # If the public path exists, delete the folder
    # and all of its contents.
    if os.path.exists(public_path):
        print("Deleting ./public/ folder")
        shutil.rmtree(public_path)
