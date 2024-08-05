import os

# Make sure static and public directories exist
static_dir = "../static/"
images_dir = "../static/images/"
public_dir = "../public/"


def check_static_folder(dir):
    if not os.path.exists(dir):
        raise FileNotFoundError("Static folder not found")


def check_images_folder(dir):
    if not os.path.exists(dir):
        raise FileNotFoundError("Static folder not found")


def check_public_folder(dir):
    if not os.path.exists(dir):
        raise FileNotFoundError("Public folder not found")


# TODO: write a recurisve function that copies all contents from static to public
