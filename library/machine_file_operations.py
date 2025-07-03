import os
import android_scripts_python.library.log_functions as log_functions
from typing import Optional
import subprocess

def format_message(msg: str, level: Optional[str] = None):
    print(f"[{level or ''}] {msg}")

def check_machine_sub_folder(main_folder: str, subfolder: str) -> Optional[str]:
    path = os.path.join(main_folder, subfolder)
    if os.path.isdir(path):
        return path
    else:
        use_default = input(f"{subfolder} folder does not exist in {main_folder} ...\n\n Do you want to install from {main_folder} instead [y/n]: ")
        if use_default.lower() == 'y':
            return main_folder
        else:
            return None

def check_machine_folder_exist(folder_path: str) -> str:
    return "yes" if os.path.isdir(folder_path) else "no"

def check_machine_file_exist(file_path: str) -> str:
    return "yes" if os.path.isfile(file_path) else "no"

def compare_machine_folder_and_files(folder1: str, file1: str, folder2: str, file2: str) -> str:
    path1 = os.path.join(folder1, file1)
    path2 = os.path.join(folder2, file2)
    if (check_machine_folder_exist(folder1) == "yes" and
        check_machine_file_exist(path1) == "yes" and
        check_machine_folder_exist(folder2) == "yes" and
        check_machine_file_exist(path2) == "yes"):
        # Use os.path.samefile if on the same filesystem
        try:
            if os.path.samefile(path1, path2):
                return "same"
            else:
                return "diff"
        except Exception:
            return "diff"
    else:
        log_functions.write_to_logs_file("compare_machine_folder_and_files did not have the valid Folder or File argument passed")
        return "invalid"

def compare_machine_files(file1: str, file2: str) -> str:
    if check_machine_file_exist(file1) == "yes" and check_machine_file_exist(file2) == "yes":
        # Use diff command for content comparison
        result = subprocess.run(["diff", "-q", file1, file2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.stdout.strip():
            return "diff"
        else:
            return "same"
    else:
        if check_machine_file_exist(file1) == "no" and check_machine_file_exist(file2) == "no":
            return "NoSrcDst"
        elif check_machine_file_exist(file1) == "no":
            return "NoSrc"
        elif check_machine_file_exist(file2) == "no":
            return "NoDst"
        else:
            return "unknown"

def build_machine_files_list(search_folder: str, search_string: str) -> list:
    # Use os.walk to find files matching the search string
    matches = []
    for root, files in os.walk(search_folder):
        for file in files:
            if search_string.lower() in file.lower():
                matches.append(os.path.join(root, file))
    return sorted(matches) 