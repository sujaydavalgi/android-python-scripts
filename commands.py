import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import android_scripts_python.library.main_functions as main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device, is_fastboot_device, is_recovery_device

def main():
    if len(sys.argv) < 2:
        commands = input("Enter the command : ").strip()
    else:
        commands = " ".join(sys.argv[1:])
    main_functions.get_device_choice()
    display_selected_device(main_functions.deviceSerial)
    if is_adb_device(main_functions.deviceSerial):
        print(" Device is in 'adb' mode")
        output = main_functions.adb_shell(main_functions.deviceSerial, *commands.split())
        print(output)
    elif is_fastboot_device(main_functions.deviceSerial) or is_recovery_device(main_functions.deviceSerial):
        print(" Device is in 'fastboot' mode")
        output = main_functions.fastboot_shell(main_functions.deviceSerial, *commands.split())
        print(output)
    else:
        print(" Device is not in 'adb' mode or 'fastboot' mode")

if __name__ == "__main__":
    main() 