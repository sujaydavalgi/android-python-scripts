import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import android_scripts_python.library.main_functions as main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device

def main():
    main_functions.get_device_choice()
    display_selected_device(main_functions.deviceSerial)
    if is_adb_device(main_functions.deviceSerial):
        grep_string = sys.argv[1] if len(sys.argv) > 1 else None
        output = main_functions.adb_shell(main_functions.deviceSerial, "logcat", "-v", "threadtime")
        if grep_string:
            for line in output.splitlines():
                if grep_string.lower() in line.lower():
                    print(line)
        else:
            print(output)
    else:
        print(" Device is not in 'adb' mode")

if __name__ == "__main__":
    main() 