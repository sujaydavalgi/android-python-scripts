import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library import main_functions
from android_scripts_python.library.device_operations import display_selected_device

def main():
    if len(sys.argv) < 2:
        main_functions.get_device_choice()
    else:
        main_functions.build_device_sn_array()
        main_functions.deviceSerial = sys.argv[1]

    display_selected_device(main_functions.deviceSerial)

    while True:
        yn = input(" Do you want to input text? [y/n] ").strip().lower()
        if yn != 'y':
            break
        inputtext = input(" --> Enter the text you want to input : ")
        # Escape spaces for adb input text
        inputtext_escaped = inputtext.replace(' ', '%s')
        main_functions.adb_shell(main_functions.deviceSerial, "shell", "input", "text", inputtext_escaped)
    print("")

if __name__ == "__main__":
    main() 