import sys
import os
import subprocess
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library.machine_file_operations import check_machine_file_exist
from android_scripts_python.library.log_functions import write_to_logs_file
from android_scripts_python.library.text_formatting import pbold
# The following should be implemented in a real APK parsing module or use aapt wrapper
# from android_scripts_python.library.apk_operations import get_machine_apk_application_name, get_machine_apk_package_name, get_machine_apk_complete_version_name

def get_machine_apk_application_name(apk_path: str) -> str:
    try:
        result = subprocess.run([
            "aapt", "dump", "badging", apk_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in result.stdout.splitlines():
            if line.startswith("application-label:"):
                return line.split(":", 1)[1].strip().strip("'")
        return "(unknown)"
    except Exception as e:
        return f"Error: {e}"

def get_machine_apk_package_name(apk_path: str) -> str:
    try:
        result = subprocess.run([
            "aapt", "dump", "badging", apk_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in result.stdout.splitlines():
            if line.startswith("package:"):
                for part in line.split():
                    if part.startswith("name="):
                        return part.split("=", 1)[1].strip("'")
        return "(unknown)"
    except Exception as e:
        return f"Error: {e}"

def get_machine_apk_complete_version_name(apk_path: str) -> str:
    try:
        result = subprocess.run([
            "aapt", "dump", "badging", apk_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in result.stdout.splitlines():
            if line.startswith("package:"):
                version_name = None
                for part in line.split():
                    if part.startswith("versionName="):
                        version_name = part.split("=", 1)[1].strip("'")
                        return version_name
        return "(unknown)"
    except Exception as e:
        return f"Error: {e}"

def main():
    if len(sys.argv) < 2:
        pbold("\n Enter the apk path : ")
        APKpath = input().strip()
    else:
        APKpath = sys.argv[1]
    print("")
    if check_machine_file_exist(APKpath) == "yes":
        print(f" Name    : {get_machine_apk_application_name(APKpath)}")
        print(f" Package : {get_machine_apk_package_name(APKpath)}")
        print(f" Version : {get_machine_apk_complete_version_name(APKpath)}")
    else:
        write_to_logs_file(f"@@ '{APKpath}' File Not Found - called from {os.path.basename(__file__)}")
        print(f" '{APKpath}' File Not Found\n")
        sys.exit(1)
    print("")

if __name__ == "__main__":
    main() 