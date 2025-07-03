import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library import main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device
from android_scripts_python.library.machine_file_operations import build_machine_files_list

def main():
    main_functions.get_device_choice()
    display_selected_device(main_functions.deviceSerial)
    if is_adb_device(main_functions.deviceSerial):
        if len(sys.argv) < 2:
            path_name = input(" Enter the Full Path: ")
        else:
            path_name = sys.argv[1]

        if os.path.isdir(path_name):
            files = build_machine_files_list(path_name, ".apk")
            if not files:
                print(f"There are no APK files in the directory: {path_name}\n")
                return
            for apk_path in files:
                apk_name = os.path.basename(apk_path)
                yn = input(f"Do you want to install [y/n] - {apk_name}: ")
                if yn.lower() == 'y':
                    print(f"\nInstalling {apk_name} ...")
                    output = main_functions.adb_shell(main_functions.deviceSerial, "wait-for-device", "install", "-r", "-d", apk_path)
                    print(output)
                    print("...Done\n")
        elif os.path.isfile(path_name):
            print(f"\nInstalling {os.path.basename(path_name)} ...")
            output = main_functions.adb_shell(main_functions.deviceSerial, "wait-for-device", "install", "-r", "-d", path_name)
            print(output)
            print("...Done\n")
        else:
            print(" Could not verify the Path type as Directory/File.\n")
    else:
        print(" Device is not in 'adb' mode\n")

if __name__ == "__main__":
    main() 