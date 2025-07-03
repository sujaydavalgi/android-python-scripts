import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import android_scripts_python.library.main_functions as main_functions
from datetime import datetime
from android_scripts_python.library.device_operations import is_google_device, get_device_name, compare_device_build_version

def write_to_logs_file(msg: str):
    print(f"LOG: {msg}")

myLogs = os.environ.get('MY_LOGS', './logs')
nowTime = datetime.now().strftime('%Y%m%d_%H%M%S')
bugreport2Extension = 'zip'
bugreportExtension = 'txt'
logcatExtension = 'txt'
screenshotExtension = 'png'
deviceScreenshotFolder = '/sdcard/Pictures/Screenshots'

def get_formatted_file_name(device_serial: str, filename: str) -> str:
    if not device_serial or device_serial == "device":
        raise ValueError(f"Invalid device serial passed to get_formatted_file_name: '{device_serial}'")
    if is_google_device(device_serial):
        return f"{get_device_name(device_serial)}_{filename}_{nowTime}"
    else:
        return f"{device_serial}_{filename}_{nowTime}"

def take_bugreport(device_serial: str, filename: str):
    compare_status = compare_device_build_version(device_serial, "7.0")
    ext = bugreport2Extension if compare_status in ("same", "greater") else bugreportExtension
    out_path = os.path.join(myLogs, f"{filename}.{ext}")
    if compare_status in ("same", "greater"):
        main_functions.adb_shell(device_serial, "shell", "bugreport", out_path)
    else:
        output = main_functions.adb_shell(device_serial, "shell", "bugreport")
        with open(out_path, "w") as f:
            f.write(output)

def get_bugreport(device_serial: str, filename: str):
    print("\n Taking Bugreport... ", end="")
    compare_status = compare_device_build_version(device_serial, "7.0")
    if compare_status in ("same", "greater"):
        print(f" {filename}.{bugreport2Extension}\n")
    else:
        print(f" {filename}.{bugreportExtension}\n")
    take_bugreport(device_serial, filename)
    print(" ...Done\n")

def save_logcat(device_serial: str, filename: str):
    out_path = os.path.join(myLogs, f"{filename}-logcat.{logcatExtension}")
    output = main_functions.adb_shell(device_serial, "shell", "logcat", "-v", "threadtime")
    with open(out_path, "w") as f:
        f.write(output)

def save_kernel_logcat(device_serial: str, filename: str):
    out_path = os.path.join(myLogs, f"{filename}-logcat_kernel.{logcatExtension}")
    output = main_functions.adb_shell(device_serial, "shell", "logcat", "-v", "threadtime", "-b", "kernel")
    with open(out_path, "w") as f:
        f.write(output)

def clear_logcat(device_serial: str):
    main_functions.adb_shell(device_serial, "shell", "logcat", "-c")

def save_screenshot_in_device(device_serial: str, filename: str):
    out_path = f"{deviceScreenshotFolder}/{filename}.{screenshotExtension}"
    main_functions.adb_shell(device_serial, "shell", "screencap", out_path)

def save_screenshot_in_machine(device_serial: str, filename: str):
    out_path = os.path.join(myLogs, f"{filename}.{screenshotExtension}")
    output = main_functions.adb_shell(device_serial, "shell", "screencap", "-p")
    with open(out_path, "wb") as f:
        f.write(output.encode())

def take_screenshot(device_serial: str, filename: str):
    save_screenshot_in_machine(device_serial, filename)

def get_screenshot(device_serial: str, filename: str):
    print("\n Taking Screenshot... ", end="")
    print(f" {filename}.{screenshotExtension}")
    take_screenshot(device_serial, filename)
    print("\n ...Done\n")

def record_device_video(device_serial: str, folder: str, file_name: str):
    """
    Records the screen of the device and saves the video in the specified folder with the given file name (no extension).
    Stops recording on KeyboardInterrupt (Ctrl+C).
    """
    import time
    import stat
    import os
    video_name = f"{file_name}.mp4"
    device_path = f"{folder}/{video_name}"
    print(f"\nINFO: Recording device screen to {device_path} (Ctrl+C to stop)...\n")
    try:
        # Start screenrecord on device
        proc = main_functions.adb_shell(device_serial, "shell", "screenrecord", device_path)
        print(" Recording... Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Stopping screenrecord...")
        # screenrecord stops on SIGINT (Ctrl+C), file is saved
        time.sleep(2)
    print(f"\n==> Screenrecord saved on device: {device_path}\n") 