import os
import shutil

from blocktype import markdown_to_html_node
from environments import BASE_DIR, CONTENT_DIR, PUBLIC_DIR, STATIC_DIR, TEMPLATE_FILE
from inline_extraction import extract_title


def check_status(directory):
    project_dir = BASE_DIR
    public_dir = os.path.join(project_dir, directory)
    if os.path.exists(public_dir):
        print("Found directory will cleanup!")
        shutil.rmtree(public_dir)
    print("Clean directory!\nCreating new public dir")
    os.mkdir(public_dir)


def copy_files(
    curr_dir=BASE_DIR,
    subdirectory=STATIC_DIR,
    curr_public_dir=os.path.join(BASE_DIR, PUBLIC_DIR),
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


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from: {from_path} to: {dest_path} using {template_path}")
    with open(from_path) as f:
        data_from_path = f.read()
    with open(template_path) as f:
        data_template_path = f.read()
    html_from_path = markdown_to_html_node(data_from_path).to_html()
    title = extract_title(data_from_path).strip()
    template_update = data_template_path.replace("{{ Title }}", title)
    template_update = template_update.strip()
    template_update = template_update.replace("{{ Content }}", html_from_path)
    template_update = template_update.replace('href="/', 'href="{basepath}')
    template_update = template_update.replace('src="/', 'src="{basepath}')
    with open(f"{dest_path}/index.html", "w") as f:
        f.write(template_update)


def generate_pages_recursively(
    dir_path_content=os.path.join(BASE_DIR, CONTENT_DIR),
    template_path=os.path.join(BASE_DIR, TEMPLATE_FILE),
    dest_dir_path=os.path.join(BASE_DIR, PUBLIC_DIR),
):
    # My first step should be to find out what content there is
    content_list_files = os.listdir(dir_path_content)
    for filename in content_list_files:
        curr_file_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(curr_file_path):
            root, ext = os.path.splitext(filename)
            if ext == ".md":
                print("Found markdown file will create html from template")
                with open(curr_file_path) as f:
                    data_from_md = f.read()
                with open(template_path) as f:
                    data_from_template = f.read()
                converted_to_html = markdown_to_html_node(data_from_md).to_html()
                html_title = extract_title(data_from_md)
                template_data_updated = data_from_template.replace(
                    "{{ Title }}", html_title
                )
                template_data_updated = template_data_updated.replace(
                    "{{ Content }}", converted_to_html
                )
                os.makedirs(
                    os.path.dirname(f"{dest_dir_path}/{root}.html"), exist_ok=True
                )
                with open(f"{dest_dir_path}/{root}.html", "w") as f:
                    f.write(template_data_updated)
        else:
            print(f"Found a directory! {filename}, will check...")
            generate_pages_recursively(
                dir_path_content=os.path.join(dir_path_content, filename),
                dest_dir_path=os.path.join(dest_dir_path, filename),
            )
