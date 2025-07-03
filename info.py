import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import android_scripts_python.library.main_functions as main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device

def main():
    main_functions.get_device_choice()
    display_selected_device(main_functions.deviceSerial)
    if is_adb_device(main_functions.deviceSerial):
        if len(sys.argv) < 2:
            output = main_functions.adb_shell(
                main_functions.deviceSerial,
                "wait-for-device", "shell", "dumpsys", "activity", "service", "BrokerService"
            )
            print(output)
        else:
            opt = sys.argv[1].lower()
            cmd = None
            if opt == "master":
                cmd = "mIsMaster"
            elif opt == "ip":
                cmd = "address:"
            elif opt == "name":
                cmd = "name:"
            elif opt == "palce":
                cmd = "placeName:"
            else:
                print("\n Invalid option in the argument...\n")
                sys.exit(1)
            output = main_functions.adb_shell(
                main_functions.deviceSerial,
                "wait-for-device", "shell", "dumpsys", "activity", "service", "BrokerService"
            )
            for line in output.splitlines():
                if cmd in line:
                    print(line)
            print("")
    else:
        print(" Device is not in 'adb' mode")

if __name__ == "__main__":
    main() 