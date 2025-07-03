import sys
import time
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library import main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device, is_fastboot_device

def main():
    if len(sys.argv) < 2:
        main_functions.get_device_choice()
    else:
        main_functions.build_device_sn_array()
        main_functions.deviceSerial = sys.argv[1]

    display_selected_device(main_functions.deviceSerial)

    if is_adb_device(main_functions.deviceSerial):
        print(" Wait for device to reboot in bootloader...", end="")
        proc = main_functions.adb_shell(main_functions.deviceSerial, "reboot", "bootloader")
        print(" Done")
        time.sleep(7)
        main_functions.build_device_sn_array()

    if is_fastboot_device(main_functions.deviceSerial):
        print("\n Wait for the device to complete wipe data and reboot...")
        main_functions.fastboot_shell(main_functions.deviceSerial, "-w")
        time.sleep(2)
        main_functions.fastboot_shell(main_functions.deviceSerial, "reboot-bootloader")
        time.sleep(2)
        main_functions.fastboot_shell(main_functions.deviceSerial, "reboot")
        print(" ")
    elif is_adb_device(main_functions.deviceSerial):
        print("\n Device is not in Fastboot mode\n")
    else:
        print("\n Unable to determine the device state \n")

if __name__ == "__main__":
    main() 