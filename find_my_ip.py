import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import android_scripts_python.library.main_functions as main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device
from android_scripts_python.library.network_operations import check_eth_wifi, get_my_ip

def main():
    if len(sys.argv) < 2:
        main_functions.get_device_choice()
    else:
        main_functions.build_device_sn_array()
        main_functions.deviceSerial = sys.argv[1]
    display_selected_device(main_functions.deviceSerial)
    if is_adb_device(main_functions.deviceSerial):
        my_connection = check_eth_wifi(main_functions.deviceSerial)
        print(f" It is connected to : {my_connection}")
        if my_connection != "None":
            print(f" IP address is : {get_my_ip(main_functions.deviceSerial)}")
    else:
        print(" Device is not in 'adb' mode")
    print("")

if __name__ == "__main__":
    main() 