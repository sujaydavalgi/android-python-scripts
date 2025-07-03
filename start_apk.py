import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library import main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device
from android_scripts_python.library.apk_operations import apk_operations
from android_scripts_python.library.text_formatting import pbold

def main():
    if len(sys.argv) < 2:
        pbold("\n Enter the apk string to search : ")
        apk_name = input().strip()
    else:
        apk_name = sys.argv[1]

    main_functions.get_device_choice()
    display_selected_device(main_functions.deviceSerial)

    if is_adb_device(main_functions.deviceSerial):
        apk_operations(main_functions.deviceSerial, apk_name, "start")
    else:
        print(" Device is not in 'adb' mode")
    print("")

if __name__ == "__main__":
    main() 