import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library import main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device
from android_scripts_python.library.main_functions import build_device_sn_array

def main():
    if len(sys.argv) < 2:
        main_functions.get_device_choice()
    else:
        build_device_sn_array()
        main_functions.deviceSerial = sys.argv[1]

    display_selected_device(main_functions.deviceSerial)

    if is_adb_device(main_functions.deviceSerial):
        adb = main_functions.adb_shell
        serial = main_functions.deviceSerial
        print(" Device Type : ", adb(serial, "wait-for-device", "shell", "getprop", "gsm.current.phone-type").strip())
        print(" Serial : ", adb(serial, "wait-for-device", "get-serialno").strip())
        print(" Manufacturer : ", adb(serial, "wait-for-device", "shell", "getprop", "ro.product.manufacturer").strip())
        print(" Model : ", adb(serial, "wait-for-device", "shell", "getprop", "ro.product.model").strip())
        print(" Android Version : ", adb(serial, "wait-for-device", "shell", "getprop", "ro.build.version.release").strip())
        print(" Android Build : ", adb(serial, "wait-for-device", "shell", "getprop", "ro.build.id").strip())
        print(" IMEI : ", adb(serial, "wait-for-device", "shell", "getprop", "ro.gsm.imei").strip())
        print()
    else:
        print(" Device is not in 'adb' mode")

if __name__ == "__main__":
    main() 