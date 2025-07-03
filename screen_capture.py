import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from android_scripts_python.library import main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device
from android_scripts_python.library.log_functions import get_formatted_file_name, get_screenshot

def main():
    main_functions.get_device_choice()
    display_selected_device(main_functions.deviceSerial)

    if is_adb_device(main_functions.deviceSerial):
        if len(sys.argv) < 2:
            file_name = input(" Enter the Screenshot File name : ").strip()
            print()
        else:
            file_name = sys.argv[1]
        file_name = get_formatted_file_name(main_functions.deviceSerial, file_name)
        print(" Your file will be saved in folder : logs\n")
        get_screenshot(main_functions.deviceSerial, file_name)
    else:
        print(" Device is not in adb mode\n")

if __name__ == "__main__":
    main() 