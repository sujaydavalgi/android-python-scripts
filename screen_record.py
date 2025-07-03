import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library import main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device
from android_scripts_python.library.log_functions import get_formatted_file_name
from android_scripts_python.library.log_functions import record_device_video
from android_scripts_python.library.text_formatting import pbold

RECORD_FOLDER = "/sdcard"

def main():
    if len(sys.argv) < 2:
        pbold("\n Enter the Video File name : ")
        file_name = input().strip()
    else:
        file_name = sys.argv[1]

    main_functions.get_device_choice()
    display_selected_device(main_functions.deviceSerial)

    if is_adb_device(main_functions.deviceSerial):
        file_name = get_formatted_file_name(main_functions.deviceSerial, file_name)
        print(f" Your video will be saved in {RECORD_FOLDER} as : {file_name}.mp4\n")
        record_device_video(main_functions.deviceSerial, RECORD_FOLDER, file_name)
    else:
        print(" Device is not in adb mode\n")

if __name__ == "__main__":
    main() 