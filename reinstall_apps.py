import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library import main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device, is_at_home_device
from android_scripts_python.library.machine_file_operations import build_machine_files_list
from android_scripts_python.library.configure_machine import myAppDir
from android_scripts_python.library.apk_operations import apk_operations
from android_scripts_python.library.text_formatting import pbold, format_message


def uninstall_all_apks(device_serial):
    # Uninstall all user-installed APKs
    output = main_functions.adb_shell(device_serial, "shell", "pm", "list", "packages", "-3")
    pkgs = [line.split(":")[-1].strip() for line in output.splitlines() if line.strip()]
    for pkg in pkgs:
        format_message(f"Uninstalling {pkg} ...", "W")
        main_functions.adb_shell(device_serial, "shell", "uninstall", pkg)


def install_all_apks_from_folder(device_serial, folder):
    files = build_machine_files_list(folder, ".apk")
    if not files:
        format_message(f"There are no APK files in the directory: {folder}\n", "E")
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
    if not is_adb_device(main_functions.deviceSerial):
        format_message(" Device is not in adb mode", "E")
        return
    if is_at_home_device(main_functions.deviceSerial):
        format_message(" Installing Apps is not allowed in @Home device ...\n", "E")
        return
    if len(sys.argv) < 2:
        pbold("\n Enter the Folder name (Case-sensitive) : ")
        build = input().strip()
    else:
        build = sys.argv[1]
    folder_path = os.path.join(myAppDir, build)
    if not os.path.isdir(folder_path):
        format_message(f"Subfolder '{build}' does not exist in {myAppDir}\n", "E")
        return
    uninstall_all_apks(main_functions.deviceSerial)
    install_all_apks_from_folder(main_functions.deviceSerial, folder_path)

if __name__ == "__main__":
    main() 