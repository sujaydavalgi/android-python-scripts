import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library.text_formatting import format_message
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device
import android_scripts_python.library.main_functions as main_functions

def main():
    if len(sys.argv) < 2:
        main_functions.get_device_choice()
    else:
        main_functions.build_device_sn_array()
        main_functions.deviceSerial = sys.argv[1]
    display_selected_device(main_functions.deviceSerial)
    if is_adb_device(main_functions.deviceSerial):
        format_message(" Clearing Logcat... ", "M")
        main_functions.adb_shell(main_functions.deviceSerial, "shell", "logcat", "-c")
        format_message("Done \n\n", "M")
    else:
        print(" Device is not in 'adb' mode")

if __name__ == "__main__":
    main() 