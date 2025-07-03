import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import android_scripts_python.library.main_functions as main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device
import android_scripts_python.library.keycode_events as keycode_events

def main():
    if len(sys.argv) < 2:
        main_functions.get_device_choice()
    else:
        main_functions.build_device_sn_array()
        main_functions.deviceSerial = sys.argv[1]
    display_selected_device(main_functions.deviceSerial)
    if not is_adb_device(main_functions.deviceSerial):
        print(" Device is not in 'adb' mode")
        return
    deviceSerial = main_functions.deviceSerial
    inputevent = None
    while inputevent != 'x':
        inputevent = input(" (u)p (d)own (l)eft (r)ight (c)enter (b)ack (h)ome (e)nter (D)el (t)ext (a)ccessory-button (p)ower e(x)it : ").strip()
        if inputevent in ['u', 'U']:
            keycode_events.keycode_dpad_up(deviceSerial)
        elif inputevent == 'd':
            keycode_events.keycode_dpad_down(deviceSerial)
        elif inputevent in ['l', 'L']:
            keycode_events.keycode_dpad_left(deviceSerial)
        elif inputevent in ['r', 'R']:
            keycode_events.keycode_dpad_right(deviceSerial)
        elif inputevent in ['c', 'C']:
            keycode_events.keycode_dpad_center(deviceSerial)
        elif inputevent in ['b', 'B']:
            keycode_events.keycode_back(deviceSerial)
        elif inputevent in ['h', 'H']:
            keycode_events.keycode_home(deviceSerial)
        elif inputevent in ['e', 'E']:
            keycode_events.keycode_enter(deviceSerial)
        elif inputevent == 'D':
            keycode_events.keycode_del(deviceSerial)
        elif inputevent in ['a', 'A']:
            keycode_events.accessory_button(deviceSerial)
        elif inputevent in ['p', 'P']:
            keycode_events.keycode_power(deviceSerial)
        elif inputevent in ['t', 'T']:
            inputtext = input(" Enter the text you want to input : ").strip()
            main_functions.adb_shell(deviceSerial, "shell", "input", "text", inputtext)

if __name__ == "__main__":
    main() 