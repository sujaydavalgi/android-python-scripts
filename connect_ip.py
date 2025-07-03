import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import android_scripts_python.library.main_functions as main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device, is_at_home_device
from android_scripts_python.library.network_operations import get_device_ip

def main():
    if len(sys.argv) < 2:
        main_functions.get_device_choice()
    else:
        main_functions.build_device_sn_array()
        main_functions.deviceSerial = sys.argv[1]
    display_selected_device(main_functions.deviceSerial)
    setPort = "5555"
    if is_adb_device(main_functions.deviceSerial):
        deviceIP = get_device_ip(main_functions.deviceSerial)
        if is_at_home_device(main_functions.deviceSerial):
            setPort = main_functions.adb_shell(main_functions.deviceSerial, "shell", "getprop", "persist.adb.tcp.port").strip()
        else:
            main_functions.adb_shell(main_functions.deviceSerial, "tcpip", setPort)
        main_functions.adb_shell(main_functions.deviceSerial, "shell", "stop", "adbd")
        main_functions.adb_shell(main_functions.deviceSerial, "shell", "start", "adbd")
        print(f" My IP : {deviceIP}")
        print(f" My port: {setPort}")
        main_functions.adb_shell(main_functions.deviceSerial, "root")
        main_functions.adb_shell(main_functions.deviceSerial, "shell", "setprop", "persist.adb.tcp.port", setPort)
        main_functions.adb_shell(main_functions.deviceSerial, "connect", f"{deviceIP}:{setPort}")
    else:
        print(" Device is not in 'adb' mode")
    print("")

if __name__ == "__main__":
    main() 