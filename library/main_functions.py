import os
import subprocess
from datetime import datetime
from typing import List
from android_scripts_python.library.text_formatting import pbold, format_message, TXT_RST, TXT_PUR
import android_scripts_python.library.log_functions as log_functions

# Stubbed config variables (should be set or imported from config)
myLogs = os.environ.get('MY_LOGS', './logs')
myAppDir = os.environ.get('MY_APP_DIR', './apps')
myLocal = os.environ.get('MY_LOCAL', './local')
myScriptsDebian = os.environ.get('MY_SCRIPTS_DEBIAN', './scripts_debian')
myScriptsOSX = os.environ.get('MY_SCRIPTS_OSX', './scripts_osx')
myOS = os.environ.get('MY_OS', 'linux')

nowTime = datetime.now().strftime('%H%M%S')
nowDate = datetime.now().strftime('%Y%m%d')
nowDateTime = datetime.now().strftime('%Y%m%d%H%M%S')

myScripts = myScriptsDebian if myOS == 'linux' else myScriptsOSX
myShellScripts = os.path.join(myScripts, 'Shell')
myPythonScripts = os.path.join(myScripts, 'Python')
myScriptLogsDir = os.path.join(myShellScripts, 'logs')
myScriptLogsFile = os.path.join(myScriptLogsDir, f'scriptLog-{nowDate}.txt')

# Ensure log directories exist
def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

ensure_dir(myLogs)
ensure_dir(myAppDir)
ensure_dir(myScriptLogsDir)

# Device arrays and globals
import android_scripts_python.library.main_functions as main_functions
DEVICE_ARRAY: List[str] = []
DEVICE_ARRAY_STATUS: List[str] = []
DEVICE_COUNT: int = 0
DEVICE_ARRAY_INDEX: int = 0
deviceSerial: str = ''

# Build device serial number array
def build_device_sn_array():
    global DEVICE_ARRAY, DEVICE_ARRAY_STATUS, DEVICE_COUNT
    DEVICE_ARRAY = []
    DEVICE_ARRAY_STATUS = []
    build_adb_devices()
    build_fastboot_devices()
    DEVICE_COUNT = len(DEVICE_ARRAY)

# Append adb devices
def build_adb_devices():
    global DEVICE_ARRAY, DEVICE_ARRAY_STATUS
    try:
        output = adb_shell(None, "devices")
        lines = output.strip().split('\n')[1:]  # skip the first line
        for line in lines:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            serial, status = parts[0], parts[1]
            if status in ["device", "recovery", "unauthorized", "offline"]:
                DEVICE_ARRAY.append(serial)
                if status == "device":
                    DEVICE_ARRAY_STATUS.append("adb")
                else:
                    DEVICE_ARRAY_STATUS.append(status)
    except Exception as e:
        log_functions.write_to_logs_file(f"Error building adb devices: {e}")

# Append fastboot devices
def build_fastboot_devices():
    global DEVICE_ARRAY, DEVICE_ARRAY_STATUS
    try:
        output = fastboot_shell(None, "devices")
        lines = output.strip().split('\n')
        for line in lines:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            serial, status = parts[0], parts[1]
            if status == "fastboot":
                DEVICE_ARRAY.append(serial)
                DEVICE_ARRAY_STATUS.append(status)
    except Exception as e:
        log_functions.write_to_logs_file(f"Error building fastboot devices: {e}")

def append_build_info(device_serial: str):
    try:
        print(adb_shell(device_serial, "shell", "getprop", "ro.build.description"))
    except Exception as e:
        log_functions.write_to_logs_file(f"Error appending build info: {e}")

def display_device_list():
    global DEVICE_COUNT
    if DEVICE_COUNT > 0:
        print("")
        for i, serial in enumerate(DEVICE_ARRAY):
            j = i + 1
            print(f" {j}. {serial}", end='')
            status = DEVICE_ARRAY_STATUS[i]
            if status in ["recovery", "fastboot", "offline", "unauthorized"]:
                print(f" - {status}")
            elif status == "adb":
                try:
                    model = adb_shell(serial, "shell", "getprop", "ro.product.model")
                    hw_code = adb_shell(serial, "shell", "getprop", "ro.hardware")
                    print(f"{TXT_RST} - {TXT_PUR}{model}{TXT_RST} ({hw_code})")
                except Exception:
                    print("")
            else:
                print("")
    else:
        print("\n There are no devices connected to the USB.\n")

def check_device_choice_validity(choice: str):
    global DEVICE_ARRAY_INDEX
    try:
        idx = int(choice)
        if idx < 1 or idx > DEVICE_COUNT:
            print(f" Dude '{choice}' is not in this list and you know it. Come on.\n")
            get_device_choice()
        else:
            DEVICE_ARRAY_INDEX = idx - 1
    except ValueError:
        print(f" Come on Dude, pick a number. '{choice}' is not a number.\n")
        get_device_choice()

def get_device_choice():
    global deviceSerial, DEVICE_ARRAY_INDEX
    build_device_sn_array()
    DEVICE_CHOICE = "0"
    if DEVICE_COUNT > 0:
        if DEVICE_COUNT > 1:
            display_device_list()
            pbold(f"\n Enter Choice [1 - {DEVICE_COUNT}] : ")
            DEVICE_CHOICE = input().strip()
            check_device_choice_validity(DEVICE_CHOICE)
            deviceSerial = DEVICE_ARRAY[DEVICE_ARRAY_INDEX]
        else:
            print("\n There is only 1 device connected to the USB\n")
            deviceSerial = DEVICE_ARRAY[0]
    else:
        print("\n There are no devices connected to the USB.\n\n")
        exit(1)

def get_device_serial() -> str:
    global deviceSerial
    return deviceSerial

def set_device_serial(serial: str):
    global deviceSerial
    deviceSerial = serial 

def get_index(device_serial: str) -> int:
    try:
        serials = [s.strip() for s in main_functions.DEVICE_ARRAY]
        idx = serials.index(device_serial.strip())
        return idx
    except ValueError:
        format_message("\n Lost the Device OR Device not Found\n", "E")
        print("DEVICE_ARRAY:", DEVICE_ARRAY)
        print("Selected deviceSerial:", device_serial)
        raise 

def adb_shell(serial, *args):
    cmd = ["adb"]
    if serial is not None:
        # cmd += ["-s", serial, "wait-for-device", "shell"]
        cmd += ["-s", serial, "wait-for-device"]
    cmd += list(args)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

def fastboot_shell(serial, *args):
    cmd = ["fastboot"]
    if serial is not None:
        cmd += ["-s", serial]
    cmd += list(args)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    result = subprocess.run([
        "fastboot", *args
    ], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip() 