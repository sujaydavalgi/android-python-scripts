import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library import main_functions
from android_scripts_python.library.device_operations import (
    display_selected_device, is_adb_device, is_fastboot_device, is_device_build_dev_key
)

def main():
    if len(sys.argv) < 2:
        main_functions.get_device_choice()
    else:
        main_functions.build_device_sn_array()
        main_functions.deviceSerial = sys.argv[1]

    display_selected_device(main_functions.deviceSerial)

    if is_adb_device(main_functions.deviceSerial):
        if is_device_build_dev_key(main_functions.deviceSerial):
            main_functions.adb_shell(main_functions.deviceSerial, "root")
            main_functions.adb_shell(main_functions.deviceSerial, "shell", "stop")
            main_functions.adb_shell(main_functions.deviceSerial, "shell", "start")
        else:
            print(" Device doesnot support root access\n")
    elif is_fastboot_device(main_functions.deviceSerial):
        main_functions.fastboot_shell(main_functions.deviceSerial, "reboot")
    else:
        print(" Device is not in 'adb' or 'fastboot' mode\n")

if __name__ == "__main__":
    main() 