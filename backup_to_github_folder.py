import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library.main_functions import myShellScripts
from android_scripts_python.library.text_formatting import pbold
from android_scripts_python.library.machine_file_operations import compare_machine_files

def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

def compare_and_copy_machine_files(src_folder, dest_folder, pattern):
    # Copy all files matching pattern from src_folder to dest_folder if they differ
    for root, files in os.walk(src_folder):
        for file in files:
            if pattern == '*.*' or pattern in file:
                src_file = os.path.join(root, file)
                rel_path = os.path.relpath(src_file, src_folder)
                dest_file = os.path.join(dest_folder, rel_path)
                ensure_dir(os.path.dirname(dest_file))
                if not os.path.exists(dest_file) or compare_machine_files(src_file, dest_file) == 'diff':
                    pbold(f"Copying {src_file} to {dest_file}\n")
                    try:
                        import shutil
                        shutil.copy2(src_file, dest_file)
                    except Exception as e:
                        print(f"Error copying {src_file} to {dest_file}: {e}")

def backup_files(source_folder, dest_folder):
    print(f" Source: {source_folder}")
    print(f" Destination: {dest_folder}")
    ensure_dir(dest_folder)
    compare_and_copy_machine_files(source_folder, dest_folder, '*.*')

def main():
    gitHubFolder = os.path.expanduser('~/Setup/GitHub')
    gitHubFolder_shell = os.path.join(gitHubFolder, 'android-shell-scripts')

    print(">> Checking Library Files ...")
    sourceFolder = os.path.join(myShellScripts, 'library')
    destFolder = os.path.join(gitHubFolder_shell, 'library')
    backup_files(sourceFolder, destFolder)
    print(">> Done checking Library Files\n")

    print(">> Checking Script Files ...")
    sourceFolder = myShellScripts
    destFolder = gitHubFolder_shell
    backup_files(sourceFolder, destFolder)
    print(">> Done checking Script Files\n")

if __name__ == "__main__":
    main() 