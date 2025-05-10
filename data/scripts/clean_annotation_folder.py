import os
import argparse
import shutil


def delete_empty_folders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Skip non-regular files
            if not os.path.isfile(file_path):
                continue

            with open(file_path, 'r') as f:
                lines = f.readlines()

            if not lines:
                os.remove(file_path)
                print(f"Removed empty file: {file_path}")
                continue

        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"Removed empty directory: {dir_path}")


def minify_annotation_folder(folder_path, skip_first_char = False):
    backup_path = os.path.join(folder_path, "..", "minified_annotations")
    if os.path.exists(backup_path):
        shutil.rmtree(backup_path)
    shutil.copytree(folder_path, backup_path)
    print(f"Backup created at: {backup_path}")

    for root, dirs, files in os.walk(backup_path, topdown=False):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            # Skip non-regular files
            if not os.path.isfile(file_path):
                continue
            with open(file_path, 'r') as f:
                lines = f.readlines()

            first_char = lines[0][0]
            if first_char == '>' or skip_first_char:
                # Filter out lines starting with '!'
                new_lines = [
                    line[1:] for line in lines if not line.startswith('!')]

                if new_lines:
                    with open(file_path, 'w') as f:
                        f.writelines(new_lines)
                    print(f"Cleaned file: {file_path}")
                else:
                    os.remove(file_path)
                    print(f"Removed file (all lines were '!'): {file_path}")

            else:
                os.remove(file_path)
                print(f"Removed file not starting with '>': {file_path}")

        # Remove empty directories after processing files
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"Removed empty directory: {dir_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Clean and filter files in an annotation folder.")
    parser.add_argument("folder", help="Path to the annotation folder")
    parser.add_argument("-skip-first", type=bool, help="Skip first char", default=False)
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"Error: '{args.folder}' is not a valid directory.")
        return

    # delete_empty_folders(args.folder)
    minify_annotation_folder(args.folder, args.skip_first)


if __name__ == "__main__":
    main()
