import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library import main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device, is_at_home_device
from android_scripts_python.library.device_file_operations import search_and_pull_device_files_from_folder

SCREENSHOT_FOLDER = "/sdcard/Pictures/Screenshots"
SEARCH_FOR_FILE = ".jpg,.png"

def main():
    if len(sys.argv) < 2:
        main_functions.get_device_choice()
    else:
        main_functions.build_device_sn_array()
        main_functions.deviceSerial = sys.argv[1]

    display_selected_device(main_functions.deviceSerial)

    if is_adb_device(main_functions.deviceSerial):
        if is_at_home_device(main_functions.deviceSerial):
            print(" There is no Screenshot folder in @Home device\n")
        else:
            search_and_pull_device_files_from_folder(main_functions.deviceSerial, SCREENSHOT_FOLDER, SEARCH_FOR_FILE)
    else:
        print(" Device is not in 'adb' mode\n")

if __name__ == "__main__":
    main() 