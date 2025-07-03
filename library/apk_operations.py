import android_scripts_python.library.main_functions as main_functions
import android_scripts_python.library.log_functions as log_functions
from android_scripts_python.library.text_formatting import format_message
from android_scripts_python.library.device_operations import is_adb_device, is_device_build_dev_key
from typing import List, Optional

# Globals (if needed)
apk_device_path = ""
apk_package_name = ""
search_apk_count = 0
apk_array: List[str] = []
apk_array_index = 0
apk_version_array: List[str] = []
apk_version_count = 0

def search_apk(device_serial: str, apk_name: str):
    global apk_array, search_apk_count
    apk_array = []
    output = main_functions.adb_shell(device_serial, "shell", "pm", "list", "packages", "-f")
    for line in output.splitlines():
        if apk_name.lower() in line.lower():
            apk_array.append(line.strip())
    search_apk_count = len(apk_array)

def split_apk_path(apk_path_str: str):
    global apk_device_path, apk_package_name
    try:
        parts = apk_path_str.split(":", 1)[1]
        apk_device_path = "=".join(parts.split("=")[:-1]).strip()
        apk_package_name = parts.split("=")[-1].strip()
    except Exception as e:
        log_functions.write_to_logs_file(f"Error splitting APK path: {e}")
        apk_device_path = ""
        apk_package_name = ""

def display_apk_list():
    if search_apk_count == 1:
        format_message(" There is only 1 APK/Package with matching string :\n\n", "W")
        split_apk_path(apk_array[0])
        format_message(f" 1. {apk_package_name} - {apk_device_path}\n")
    elif search_apk_count > 1:
        format_message(" Following APKs/Packages found with matching string : \n\n", "I")
        for i, apk in enumerate(apk_array):
            split_apk_path(apk)
            format_message(f" {i+1}. {apk_package_name} - {apk_device_path}\n")
    else:
        format_message(" There are no APKs/Packages installed having that string\n", "E")

def check_apk_choice_validity(choice: str):
    global apk_array_index
    if not choice.isdigit():
        format_message(f" Come on Dude, pick a number. '{choice}' is not a number.\n", "W")
        log_functions.write_to_logs_file(f" Entered '{choice}' instead of a number")
        raise ValueError("Choice is not a number")
    idx = int(choice)
    if idx < 1 or idx > search_apk_count:
        format_message(f" Dude '{choice}' is not choice in this list and you know it. Come on.\n", "W")
        log_functions.write_to_logs_file(f" Entered '{choice}' which was not in choice range '{search_apk_count}'")
        raise ValueError("Choice out of range")
    apk_array_index = idx - 1

def apk_operations(device_serial: str, apk_name: str, operation: str):
    search_apk(device_serial, apk_name)
    if search_apk_count > 0:
        display_apk_list()
        if search_apk_count > 1:
            choice = input("\n Enter APK Choice : ")
            print()
            check_apk_choice_validity(choice)
            apk_path = apk_array[apk_array_index]
        else:
            apk_path = apk_array[0]
        split_apk_path(apk_path)
        op = operation.strip().upper()
        if op == "PULL":
            pull_device_app(device_serial, apk_device_path)
        elif op == "CLEAR":
            clear_device_app(device_serial, apk_package_name)
        elif op == "STOP":
            stop_device_app(device_serial, apk_package_name)
        elif op == "KILL":
            kill_device_app(device_serial, apk_package_name)
        elif op == "START":
            start_device_apk(device_serial, apk_package_name)
        elif op == "RESTART":
            restart_device_app(device_serial, apk_package_name)
        elif op == "UNINSTALL":
            uninstall_selected_device_app(device_serial, apk_path)
        elif op == "UNINSTALLUPDATES":
            uninstall_device_app_updates(device_serial, apk_package_name)
        elif op == "VERSION":
            get_device_app_version(device_serial, apk_package_name)
        else:
            log_functions.write_to_logs_file(f" Unsupported argument '{operation}' passed to apk_operations()")
            format_message(f" Unsupported argument passed to apk_operations()", "E")
    else:
        format_message(" No APKs installed with that name\n", "E")

def app_pid(device_serial: str, package_name: str) -> Optional[str]:
    output = main_functions.adb_shell(device_serial, "shell", "ps")
    for line in output.splitlines():
        if package_name in line:
            return line.split()[1]
    return None

def kill_device_app(device_serial: str, package_name: str):
    pid = app_pid(device_serial, package_name)
    if pid:
        main_functions.adb_shell(device_serial, "shell", "kill", pid)

def pull_device_app(device_serial: str, device_path: str):
    dst_folder = "."  # Placeholder
    format_message(f" Your files will be saved in folder : {dst_folder}", "M")
    format_message("\n Pulling APK...", "I")
    main_functions.adb_shell(device_serial, "shell", "pull", device_path, dst_folder)

def clear_device_app(device_serial: str, package_name: str):
    if is_adb_device(device_serial):
        format_message(f" Clearing APK {package_name} data\n", "W")
        main_functions.adb_shell(device_serial, "shell", "pm", "clear", package_name)
    else:
        format_message(" Device is not in adb mode\n", "E")

def uninstall_selected_device_app(device_serial: str, apk_path: str):
    split_apk_path(apk_path)
    format_message("\n Uninstalling APK...\n", "W")
    if is_adb_device(device_serial):
        format_message(f" {apk_device_path} - {apk_package_name}\n")
        main_functions.adb_shell(device_serial, "shell", "uninstall", apk_package_name)
        format_message(" Trying to delete the file...\n", "W")
        if is_device_build_dev_key(device_serial):
            main_functions.adb_shell(device_serial, "shell", "root")
            main_functions.adb_shell(device_serial, "shell", "remount")
            main_functions.adb_shell(device_serial, "shell", "rm", "-rf", apk_device_path)
            format_message("Done\n\n Rebooting...")
            main_functions.adb_shell(device_serial, "shell", "reboot")
        else:
            format_message(" Device doesnot support root access\n", "E")
    else:
        format_message(" Device is not in adb mode\n", "E")

def uninstall_device_app_updates(device_serial: str, package_name: str):
    if is_adb_device(device_serial):
        format_message(f" Uninstall App {package_name} updates\n", "W")
        main_functions.adb_shell(device_serial, "shell", "pm", "uninstall", package_name)
    else:
        format_message(" Device is not in adb mode\n", "E")

def uninstall_device_app_updates_prompt(device_serial: str, package_name: str):
    main_functions.adb_shell(device_serial, "shell", "am", "start", "-a", "android.intent.action.DELETE", "-d", f"package:{package_name}")

def start_device_apk(device_serial: str, package_name: str):
    main_functions.adb_shell(device_serial, "shell", "am", "start", package_name)

def stop_device_app(device_serial: str, package_name: str):
    main_functions.adb_shell(device_serial, "shell", "am", "force-stop", package_name)

def restart_device_app(device_serial: str, package_name: str):
    stop_device_app(device_serial, package_name)
    start_device_apk(device_serial, package_name)

def get_device_app_version(device_serial: str, package_name: str):
    global apk_version_array, apk_version_count
    apk_version_array = []
    output = main_functions.adb_shell(device_serial, "shell", "dumpsys", "package", package_name)
    for line in output.splitlines():
        if "versionName" in line:
            version = line.split("=", 1)[-1].strip()
            apk_version_array.append(version)
    apk_version_count = len(apk_version_array)
    format_message(" Installed version(s):\n", "I")
    if apk_version_count > 0:
        format_message(f" 1. Current installed Version - {apk_version_array[0]}\n")
        if apk_version_count > 1:
            format_message(f" 2. System default Version - {apk_version_array[1]}\n") 