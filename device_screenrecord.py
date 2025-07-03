import sys
import os
import time
import stat
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import android_scripts_python.library.main_functions as main_functions
from android_scripts_python.library.device_operations import display_selected_device, is_adb_device

def error_exit(msg):
    print(f"error: {msg}")
    sys.exit(1)

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: {os.path.basename(sys.argv[0])} name <device_id>")
        sys.exit(1)
    keyword = sys.argv[1]
    if len(sys.argv) == 3:
        main_functions.build_device_sn_array()
        main_functions.deviceSerial = sys.argv[2]
    else:
        main_functions.get_device_choice()
    display_selected_device(main_functions.deviceSerial)
    if not is_adb_device(main_functions.deviceSerial):
        error_exit("Device is not in 'adb' mode")
    screenshot_dir = "screenrecord"
    filename = time.strftime(f"%y%m%d-{keyword}.mp4")
    screenshot_path = os.path.join(screenshot_dir, filename)
    if not os.path.isdir(screenshot_dir):
        os.makedirs(screenshot_dir, exist_ok=True)
        os.chmod(screenshot_dir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    if os.path.exists(screenshot_path):
        error_exit(f"File {screenshot_path} already exists! Use a different keyword.")
    sdcard_dir = "/sdcard/screenrecord"
    main_functions.adb_shell(main_functions.deviceSerial, "shell", "mkdir", "-p", sdcard_dir)
    sdcard_path = f"{sdcard_dir}/{filename}"
    # Start screenrecord in background
    main_functions.adb_shell(main_functions.deviceSerial, "shell", "screenrecord", "--bugreport", sdcard_path, "&")
    def get_pid():
        ps_out = main_functions.adb_shell(main_functions.deviceSerial, "shell", "ps")
        for line in ps_out.splitlines():
            if "screenrecord" in line:
                return line.split()[1]
        return None
    pid = get_pid()
    if not pid:
        error_exit("screenrecord process not found. exit")
    input("Press [enter] to stop screenrecord")
    print("\nINFO: Waiting for recording to be done...")
    # Try to kill the process (requires root)
    main_functions.adb_shell(main_functions.deviceSerial, "shell", "su", "0", "sh", "-c", f"kill -2 {pid}")
    time.sleep(3)
    main_functions.adb_shell(main_functions.deviceSerial, "pull", sdcard_path, screenshot_path)
    os.chmod(screenshot_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    print(f"\n==> Screenrecord is available here :  {os.path.abspath(screenshot_path)}\n")

if __name__ == "__main__":
    main() 