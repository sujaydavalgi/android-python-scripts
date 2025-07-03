import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library.main_functions import get_device_choice, get_device_serial
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device
from android_scripts_python.library.text_formatting import pbold, TXT_RST
from android_scripts_python.library.log_functions import get_bugreport, get_formatted_file_name
from android_scripts_python.library.main_functions import myLogs

def main():
    get_device_choice()
    deviceSerial = get_device_serial()
    display_selected_device(deviceSerial)
    if is_adb_device(deviceSerial):
        if len(sys.argv) < 2:
            pbold(" Enter the Bugreport File name : ", end='')
            fileName = input().strip()
            print()
        else:
            fileName = sys.argv[1]
        # print(f"DEBUG: deviceSerial = '{deviceSerial}'")
        fileName = get_formatted_file_name(deviceSerial, fileName)
        print(f" Your file will be saved in folder : {myLogs}")
        get_bugreport(deviceSerial, fileName)
    else:
        print(" Device is not in 'adb' mode\n")
    print("\n")

if __name__ == "__main__":
    main() 