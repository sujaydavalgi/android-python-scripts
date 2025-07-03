import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library import main_functions
from android_scripts_python.library.device_operations import (
    display_selected_device, is_adb_device, is_fastboot_device, is_recovery_device
)

def main():
    if len(sys.argv) < 2:
        main_functions.get_device_choice()
    else:
        main_functions.build_device_sn_array()
        main_functions.deviceSerial = sys.argv[1]

    display_selected_device(main_functions.deviceSerial)

    if is_adb_device(main_functions.deviceSerial):
        main_functions.adb_shell(main_functions.deviceSerial, "reboot", "recovery")
    elif is_fastboot_device(main_functions.deviceSerial):
        main_functions.fastboot_shell(main_functions.deviceSerial, "reboot", "recovery")
    elif is_recovery_device(main_functions.deviceSerial):
        print(" Device is already in 'Recovery' mode")
    else:
        print(" Device is not in 'adb' mode")

if __name__ == "__main__":
    main() 