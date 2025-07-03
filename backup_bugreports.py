import os
import sys
import shutil
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from android_scripts_python.library.main_functions import myLogs, myLocal
from android_scripts_python.library.text_formatting import TXT_GRN, TXT_BLD, TXT_RST

def main():
    if os.path.abspath(myLogs) == os.path.abspath(myLocal):
        print(" You are already using the local drive. No need to backup\n")
    else:
        files = os.listdir(myLogs)
        if files:
            print(f"\n Moving From : {myLogs}")
            print(f" Moving To   : {myLocal}")
            print("\n Started moving...", end='')
            for f in files:
                src = os.path.join(myLogs, f)
                dst = os.path.join(myLocal, f)
                shutil.move(src, dst)
            print(f"{TXT_GRN}{TXT_BLD} Done {TXT_RST}\n")
        else:
            print(f"\n There are no files in the folder {myLogs}\n")

if __name__ == "__main__":
    main() 