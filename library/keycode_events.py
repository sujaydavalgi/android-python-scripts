import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import android_scripts_python.library.main_functions as main_functions
import android_scripts_python.library.log_functions as log_functions

def send_key_event(device_serial: str, keycode: str):
    try:
        main_functions.adb_shell(device_serial, "shell", "input", "keyevent", keycode)
    except Exception as e:
        log_functions.write_to_logs_file(f"Failed to send key event {keycode} to {device_serial}: {e}")

def keycode_unknown(device_serial: str):
    send_key_event(device_serial, "KEYCODE_UNKNOWN")

def keycode_home(device_serial: str):
    send_key_event(device_serial, "KEYCODE_HOME")

def keycode_back(device_serial: str):
    send_key_event(device_serial, "KEYCODE_BACK")

def keycode_menu(device_serial: str):
    send_key_event(device_serial, "KEYCODE_MENU")

def keycode_app_switch(device_serial: str):
    send_key_event(device_serial, "KEYCODE_APP_SWITCH")

def keycode_volume_up(device_serial: str):
    send_key_event(device_serial, "KEYCODE_VOLUME_UP")

def keycode_volume_down(device_serial: str):
    send_key_event(device_serial, "KEYCODE_VOLUME_DOWN")

def keycode_power(device_serial: str):
    send_key_event(device_serial, "KEYCODE_POWER")

def accessory_button(device_serial: str):
    try:
        main_functions.adb_shell(device_serial, "shell", "am", "start", "-n", "com.google.android.canvas.settings/.accessories.AddAccessoryActivity")
    except Exception as e:
        log_functions.write_to_logs_file(f"Failed to start accessory activity on {device_serial}: {e}")

def keycode_sleep(device_serial: str):
    send_key_event(device_serial, "KEYCODE_SLEEP")

def keycode_wakeup(device_serial: str):
    send_key_event(device_serial, "KEYCODE_WAKEUP")

def keycode_pairing(device_serial: str):
    send_key_event(device_serial, "KEYCODE_PAIRING")

def keycode_brightness_down(device_serial: str):
    send_key_event(device_serial, "KEYCODE_BRIGHTNESS_DOWN")

def keycode_brightness_up(device_serial: str):
    send_key_event(device_serial, "KEYCODE_BRIGHTNESS_UP")

def keycode_camera(device_serial: str):
    send_key_event(device_serial, "KEYCODE_CAMERA")

def keycode_focus(device_serial: str):
    send_key_event(device_serial, "KEYCODE_FOCUS")

def keycode_call(device_serial: str):
    send_key_event(device_serial, "KEYCODE_CALL")

def keycode_end_call(device_serial: str):
    send_key_event(device_serial, "KEYCODE_ENDCALL")

def keycode_star(device_serial: str):
    send_key_event(device_serial, "KEYCODE_STAR")

def keycode_pound(device_serial: str):
    send_key_event(device_serial, "KEYCODE_POUND")

def keycode_0(device_serial: str):
    send_key_event(device_serial, "KEYCODE_0")

def keycode_1(device_serial: str):
    send_key_event(device_serial, "KEYCODE_1")

def keycode_2(device_serial: str):
    send_key_event(device_serial, "KEYCODE_2")

def keycode_3(device_serial: str):
    send_key_event(device_serial, "KEYCODE_3")

def keycode_4(device_serial: str):
    send_key_event(device_serial, "KEYCODE_4")

def keycode_5(device_serial: str):
    send_key_event(device_serial, "KEYCODE_5")

def keycode_6(device_serial: str):
    send_key_event(device_serial, "KEYCODE_6")

def keycode_7(device_serial: str):
    send_key_event(device_serial, "KEYCODE_7")

def keycode_8(device_serial: str):
    send_key_event(device_serial, "KEYCODE_8")

def keycode_9(device_serial: str):
    send_key_event(device_serial, "KEYCODE_9")

# Letters
for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    exec(f"def keycode_{letter.lower()}(device_serial: str):\n    send_key_event(device_serial, 'KEYCODE_{letter}')\n")

# DPAD

def keycode_dpad_up(device_serial: str):
    send_key_event(device_serial, "KEYCODE_DPAD_UP")

def keycode_dpad_down(device_serial: str):
    send_key_event(device_serial, "KEYCODE_DPAD_DOWN")

def keycode_dpad_left(device_serial: str):
    send_key_event(device_serial, "KEYCODE_DPAD_LEFT")

def keycode_dpad_right(device_serial: str):
    send_key_event(device_serial, "KEYCODE_DPAD_RIGHT")

def keycode_dpad_center(device_serial: str):
    send_key_event(device_serial, "KEYCODE_DPAD_CENTER")

# Common symbols and controls

def keycode_enter(device_serial: str):
    send_key_event(device_serial, "KEYCODE_ENTER")

def keycode_del(device_serial: str):
    send_key_event(device_serial, "KEYCODE_DEL")

def keycode_tab(device_serial: str):
    send_key_event(device_serial, "KEYCODE_TAB")

def keycode_space(device_serial: str):
    send_key_event(device_serial, "KEYCODE_SPACE")

def keycode_comma(device_serial: str):
    send_key_event(device_serial, "KEYCODE_COMMA")

def keycode_period(device_serial: str):
    send_key_event(device_serial, "KEYCODE_PERIOD")

def keycode_minus(device_serial: str):
    send_key_event(device_serial, "KEYCODE_MINUS")

def keycode_equals(device_serial: str):
    send_key_event(device_serial, "KEYCODE_EQUALS")

def keycode_left_bracket(device_serial: str):
    send_key_event(device_serial, "KEYCODE_LEFT_BRACKET")

def keycode_right_bracket(device_serial: str):
    send_key_event(device_serial, "KEYCODE_RIGHT_BRACKET")

def keycode_backslash(device_serial: str):
    send_key_event(device_serial, "KEYCODE_BACKSLASH")

def keycode_semicolon(device_serial: str):
    send_key_event(device_serial, "KEYCODE_SEMICOLON")

def keycode_apostrophe(device_serial: str):
    send_key_event(device_serial, "KEYCODE_APOSTROPHE")

def keycode_slash(device_serial: str):
    send_key_event(device_serial, "KEYCODE_SLASH")

def keycode_at(device_serial: str):
    send_key_event(device_serial, "KEYCODE_AT")

def keycode_plus(device_serial: str):
    send_key_event(device_serial, "KEYCODE_PLUS")

def keycode_page_up(device_serial: str):
    send_key_event(device_serial, "KEYCODE_PAGE_UP")

def keycode_page_down(device_serial: str):
    send_key_event(device_serial, "KEYCODE_PAGE_DOWN")

def keycode_escape(device_serial: str):
    send_key_event(device_serial, "KEYCODE_ESCAPE")

def keycode_forward_del(device_serial: str):
    send_key_event(device_serial, "KEYCODE_FORWARD_DEL")

def keycode_ctrl_left(device_serial: str):
    send_key_event(device_serial, "KEYCODE_CTRL_LEFT")

def keycode_ctrl_right(device_serial: str):
    send_key_event(device_serial, "KEYCODE_CTRL_RIGHT")

def keycode_caps_lock(device_serial: str):
    send_key_event(device_serial, "KEYCODE_CAPS_LOCK")

def keycode_scroll_lock(device_serial: str):
    send_key_event(device_serial, "KEYCODE_SCROLL_LOCK")

def keycode_meta_left(device_serial: str):
    send_key_event(device_serial, "KEYCODE_META_LEFT")

def keycode_meta_right(device_serial: str):
    send_key_event(device_serial, "KEYCODE_META_RIGHT")

def keycode_function(device_serial: str):
    send_key_event(device_serial, "KEYCODE_FUNCTION")

def keycode_sysrq(device_serial: str):
    send_key_event(device_serial, "KEYCODE_SYSRQ") 