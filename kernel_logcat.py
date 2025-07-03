import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library import main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device
from android_scripts_python.library.log_functions import get_formatted_file_name, save_kernel_logcat

def main():
    main_functions.get_device_choice()
    display_selected_device(main_functions.deviceSerial)
    if is_adb_device(main_functions.deviceSerial):
        if len(sys.argv) < 2:
            output = main_functions.adb_shell(main_functions.deviceSerial, "logcat", "-v", "threadtime", "-b", "kernel")
            print(output)
        else:
            file_name = get_formatted_file_name(main_functions.deviceSerial, sys.argv[1])
            print(f" Your file will be saved in the logs folder as: {file_name}-logcat_kernel.txt\n")
            save_kernel_logcat(main_functions.deviceSerial, file_name)
    else:
        print(" Device is not in 'adb' mode")

if __name__ == "__main__":
    main() 