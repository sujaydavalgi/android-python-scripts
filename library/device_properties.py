import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import android_scripts_python.library.main_functions as main_functions

def get_device_android_code_name(device_serial: str) -> str:
    api_level = get_device_build_sdk_version(device_serial)
    try:
        api_level = int(api_level)
    except Exception:
        return "android"
    if api_level == 1:
        return "android_A"
    elif api_level == 2:
        return "android_B"
    elif api_level == 3:
        return "android_C"
    elif api_level == 4:
        return "android_D"
    elif api_level in [5, 6, 7]:
        return "android_E"
    elif api_level == 8:
        return "android_F"
    elif api_level in [9, 10]:
        return "android_G"
    elif api_level in [11, 12, 13]:
        return "android_H"
    elif api_level in [14, 15]:
        return "android_I"
    elif api_level in [16, 17, 18]:
        return "android_J"
    elif api_level in [19, 20]:
        return "android_K"
    elif api_level in [21, 22]:
        return "android_L"
    elif api_level == 23:
        return "android_M"
    elif api_level in [24, 25]:
        return "android_N"
    elif api_level in [26, 27]:
        return "android_O"
    elif api_level == 28:
        return "android_P"
    elif api_level == 29:
        return "android_Q"
    else:
        return "android"

def get_device_emulator_type(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "get-state").replace("\r", "").replace("\n", "")

def get_device_name(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "ro.product.device").replace("\r", "").replace("\n", "")

def get_product_name(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "ro.product.name").replace("\r", "").replace("\n", "")

def get_device_build_flavor(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "ro.build.flavor").replace("\r", "").replace("\n", "")

def get_device_build_type(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "ro.build.type").replace("\r", "").replace("\n", "")

def get_device_keys(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "ro.build.tags").replace("\r", "").replace("\n", "")

def get_device_build_sdk_version(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "ro.build.version.sdk").replace("\r", "").replace("\n", "")

def get_device_build(device_serial: str) -> str:
    desc = main_functions.adb_shell(device_serial, "shell", "getprop", "ro.build.description").replace("\r", "").replace("\n", "")
    parts = desc.split()
    if len(parts) >= 3:
        device_build = parts[2]
        if device_build == "MASTER" and len(parts) >= 4:
            device_build_no = parts[3]
            device_build = f"{device_build}-{device_build_no}"
        return device_build
    return desc

def get_device_build2(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "ro.build.id").replace("\r", "").replace("\n", "") 