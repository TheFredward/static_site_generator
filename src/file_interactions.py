import os
import shutil


def check_status(directory):
    project_dir = "/home/thefredward/workspace/thefredward/static_site_generator"
    public_dir = os.path.join(project_dir, directory)
    if os.path.exists(public_dir):
        print("Found directory will cleanup!")
        shutil.rmtree(public_dir)
    print("Clean directory!\nCreating new public dir")
    os.mkdir(public_dir)


def copy_files(
    curr_dir="/home/thefredward/workspace/thefredward/static_site_generator",
    subdirectory="static",
    curr_public_dir="/home/thefredward/workspace/thefredward/static_site_generator/public",
):
    curr_dir = os.path.join(curr_dir, subdirectory)
    if subdirectory != "static":
        curr_public_dir = os.path.join(curr_public_dir, subdirectory)
        print(f"Creating new directory for public with dir name: {subdirectory}")
        os.mkdir(curr_public_dir)
    list_items = []
    if os.path.exists(curr_dir):
        list_items = os.listdir(curr_dir)

    for item_found in list_items:
        curr_file = os.path.join(curr_dir, item_found)
        if os.path.isfile(curr_file):
            print(f"Found the following file: {item_found}")
            print(shutil.copy(curr_file, curr_public_dir))
        else:
            print(f"THis is a directory: {item_found} Moving into!")
            copy_files(curr_dir, item_found, curr_public_dir)
