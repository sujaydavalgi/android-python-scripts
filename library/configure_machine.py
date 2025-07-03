import os
import platform
from android_scripts_python.library.machine_os import check_my_os_type

# Stub variables (to be set or imported from config)
myLogs = os.environ.get('MY_LOGS', './logs')
myAppDir = os.environ.get('MY_APP_DIR', './apps')
myAAHDir = os.environ.get('MY_AAH_DIR', './AAH/apps')
myACWDir = os.environ.get('MY_ACW_DIR', './ACW/apps')
myGPMDir = os.environ.get('MY_GPM_DIR', './GPM/apps')
myLocal = os.environ.get('MY_LOCAL', './local')

myOS = platform.system().lower()

def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

#--- where it will store the bugreports, logcats, screenshots, pulled videos/images
ensure_dir(myLogs)

#--- from where it will search for the general apps
ensure_dir(myAppDir)

#--- from where it will search for the @Home apps folder
ensure_dir(myAAHDir)

#--- from where it will search for the ClockWorks apps folder
ensure_dir(myACWDir)

#--- from where it will search for the Music apps folder
ensure_dir(myGPMDir)

#--- to backup the files from NFS directory to local storage
if not os.path.isdir(myLocal):
    if check_my_os_type() == 'linux':
        ensure_dir(myLocal) 