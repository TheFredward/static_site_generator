import os
import sys

from environments import BASE_DIR, PUBLIC_DIR
from file_interactions import (
    check_status,
    copy_files,
    generate_pages_recursively,
)


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        print(f"Using the following {basepath}")
    else:
        print(f"No basepath was passed, will use default: {basepath}")

    check_status("docs")
    copy_files(curr_public_dir=os.path.join(BASE_DIR, "docs"))
    generate_pages_recursively(
        dest_dir_path=os.path.join(BASE_DIR, "docs"), base_path=basepath
    )


if __name__ == "__main__":
    main()
