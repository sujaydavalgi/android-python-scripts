import sys
import subprocess
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import android_scripts_python.library.main_functions as main_functions
from android_scripts_python.library.device_operations import display_selected_device

# You may want to set this from an environment variable or config
MY_SDK = os.environ.get('MY_SDK', '~/Android/Sdk')

def main():
    if len(sys.argv) < 2:
        main_functions.get_device_choice()
    else:
        main_functions.build_device_sn_array()
        main_functions.deviceSerial = sys.argv[1]
    display_selected_device(main_functions.deviceSerial)
    subprocess.run(["adb", "-s", main_functions.deviceSerial, "forward", "tcp:5277", "tcp:5277"])
    desktop_head_unit_path = os.path.expanduser(f"{MY_SDK}/extras/google/auto/desktop-head-unit")
    subprocess.run([desktop_head_unit_path])

if __name__ == "__main__":
    main() 