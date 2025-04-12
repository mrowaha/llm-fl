"""
this will take the executed files of the bug,
go through the original source code and retrieve only those files
while maintaining their tree structure


it is better to do the following
Copy this script to the root directory of the project
Update the empty string with the file list
execute the script inside the project root dir
mv the generated source dir to the respective data folder
"""

import shutil
from pathlib import Path


file_list = "".split("\n")


source_root = Path(".")
destination_root = Path("source")

for file_path in file_list:
    src = Path(file_path)
    relative_path = src.relative_to(source_root)
    dest = destination_root / relative_path

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"Copied {src} -> {dest}")