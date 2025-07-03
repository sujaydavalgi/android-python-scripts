import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device
from android_scripts_python.library.apk_operations import apk_operations
from android_scripts_python.library.main_functions import get_device_choice, deviceSerial

def main():
    if len(sys.argv) < 2:
        APKname = input("\n Enter the apk string to search : ").strip()
    else:
        APKname = sys.argv[1]
    get_device_choice()
    display_selected_device(deviceSerial)
    if is_adb_device(deviceSerial):
        apk_operations(deviceSerial, APKname, "version")
    else:
        print(" Device is not in 'adb' mode")
    print("")

if __name__ == "__main__":
    main() 