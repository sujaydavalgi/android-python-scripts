import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library import main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device
from android_scripts_python.library.machine_file_operations import build_machine_files_list
from android_scripts_python.library.configure_machine import myAppDir

def install_machine_files(device_serial, main_folder, sub_folder, search_string):
    folder_path = os.path.join(main_folder, sub_folder)
    if not os.path.isdir(folder_path):
        use_default = input(f"{sub_folder} folder does not exist in {main_folder} ...\n\n Do you want to install from {main_folder} instead [y/n]: ")
        if use_default.lower() == 'y':
            folder_path = main_folder
        else:
            print("Aborted.")
            return
    files = build_machine_files_list(folder_path, search_string)
    if not files:
        print(f"There are no matching files in the directory: {folder_path}\n")
        return
    for apk_path in files:
        apk_name = os.path.basename(apk_path)
        yn = input(f"Do you want to install [y/n] - {apk_name}: ")
        if yn.lower() == 'y':
            print(f"\nInstalling {apk_name} ...")
            output = main_functions.adb_shell(device_serial, "wait-for-device", "install", "-r", "-d", apk_path)
            print(output)
            print("...Done\n")

def main():
    main_functions.get_device_choice()
    display_selected_device(main_functions.deviceSerial)
    if is_adb_device(main_functions.deviceSerial):
        if len(sys.argv) < 2:
            sub_folder = input(" Enter the Folder name (Case-sensitive): ")
            search_string = "apk"
        else:
            if len(sys.argv) >= 3:
                search_string = sys.argv[2]
            else:
                search_string = "apk"
            sub_folder = sys.argv[1]
        install_machine_files(main_functions.deviceSerial, myAppDir, sub_folder, search_string)
    else:
        print(" Device not in 'adb' mode")

if __name__ == "__main__":
    main() 