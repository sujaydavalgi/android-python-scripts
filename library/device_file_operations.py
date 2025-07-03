import android_scripts_python.library.main_functions as main_functions
import android_scripts_python.library.text_formatting as text_formatting
from typing import List, Optional
import os

# Globals (if needed)
device_files_array: List[str] = []
device_files_count = 0
device_file_selected = ""
device_file_array_index = 0
myLogs = os.environ.get('MY_LOGS', './logs')

def check_device_folder(device_serial: str, folder_path: str) -> bool:
    output = main_functions.adb_shell(device_serial, "shell", "-c", f"[[ -d '{folder_path}' ]] && echo 1 || echo 0")
    return output.strip() == "1"

def check_device_file(device_serial: str, folder_path: str, file_name: str) -> bool:
    if check_device_folder(device_serial, folder_path):
        output = main_functions.adb_shell(device_serial, "shell", "-c", f"[[ -f '{folder_path}/{file_name}' ]] && echo 1 || echo 0")
        return output.strip() == "1"
    else:
        text_formatting.format_message(f"'{folder_path}' folder not found\n", "E")
        return False

def build_device_files_array(device_serial: str, folder: str, file_type: str):
    global device_files_array, device_files_count
    if not check_device_folder(device_serial, folder):
        text_formatting.format_message(f" Folder '{folder}' does not exist in the device\n\n", "E")
        raise FileNotFoundError(f"Folder '{folder}' does not exist on device")
    path_to_search = f"{folder}/" if file_type == "all" else f"{folder}/*{file_type}*"
    output = main_functions.adb_shell(device_serial, "shell", "ls", path_to_search)
    # Remove known 'not found' messages
    for not_found in ["*.jpg*: No such file or directory", "*.png*: No such file or directory", "*.mp4*: No such file or directory"]:
        output = output.replace(not_found, "")
    device_files_array = [f.strip() for f in output.splitlines() if f.strip()]
    device_files_count = len(device_files_array)

def display_device_file_list():
    for idx, file in enumerate(device_files_array, 1):
        print(f" {idx}. {file}")

def check_device_file_choice_validity(choice: str):
    global device_file_array_index
    if not choice.isdigit():
        text_formatting.format_message("\n Come on Dude! Pick a number\n\n", "W")
        raise ValueError("Choice is not a number")
    idx = int(choice)
    if idx < 1 or idx > device_files_count:
        text_formatting.format_message(f" Dude '{choice}' is not a choice in this list and you know it. Come on!\n", "W")
        raise ValueError("Choice out of range")
    device_file_array_index = idx - 1

def get_device_file_choice(device_serial: str, folder: str, file_type: str) -> Optional[str]:
    global device_file_selected
    build_device_files_array(device_serial, folder, file_type)
    if device_files_count > 0:
        if device_files_count > 1:
            display_device_file_list()
            choice = input("\n Enter Choice : ")
            check_device_file_choice_validity(choice)
            device_file_selected = device_files_array[device_file_array_index]
        else:
            text_formatting.format_message(f" There is only 1 file in the folder '{folder}'\n\n", "W")
            text_formatting.format_message(f" 1. {device_files_array[0]}\n\n")
            yn = input(" Do you want to pull it ? [y/n] : ")
            if yn.lower() == 'y':
                device_file_selected = device_files_array[0]
            else:
                device_file_selected = None
    else:
        text_formatting.format_message(f" There are no {file_type} files in the device directory : ", "E")
        text_formatting.format_message(f"{folder}\n\n")
        return None
    return device_file_selected

def search_and_pull_device_files_from_folder(device_serial: str, folder: str, file_type: str):
    file_selected = get_device_file_choice(device_serial, folder, file_type)
    if file_selected:
        text_formatting.format_message(f"\n Selected file : {file_selected}\n")
        text_formatting.format_message(f" will be saved in : {myLogs}\n")
        main_functions.adb_shell(device_serial, "shell", "pull", file_selected, myLogs)
        text_formatting.format_message("\n Done\n\n")

def pull_device_single_file_from_folder(device_serial: str, folder: str, filename: str):
    device_file_complete_path = f"{folder}/{filename}"
    main_functions.adb_shell(device_serial, "shell", "pull", device_file_complete_path, myLogs)

def pull_device_single_file_from_path(device_serial: str, file_path: str):
    main_functions.adb_shell(device_serial, "shell", "pull", file_path, myLogs)

def remove_single_file_from_path(device_serial: str, file_path: str):
    if check_device_folder(device_serial, os.path.dirname(file_path)) and check_device_file(device_serial, os.path.dirname(file_path), os.path.basename(file_path)):
        main_functions.adb_shell(device_serial, "shell", "-c", f"rm '{file_path}'")

def remove_single_file_from_folder(device_serial: str, folder: str, filename: str):
    if check_device_folder(device_serial, folder) and check_device_file(device_serial, folder, filename):
        main_functions.adb_shell(device_serial, "shell", "-c", f"rm '{folder}/{filename}'")

def remove_all_files_from_folder(device_serial: str, folder: str):
    main_functions.adb_shell(device_serial, "shell", "-c", f"rm -rf '{folder}/*.*'")

def remove_folder(device_serial: str, folder: str):
    main_functions.adb_shell(device_serial, "shell", "-c", f"rm -rf '{folder}'") 