import os
import sys
import glob
import shutil
import stat
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

home = os.path.expanduser('~')
present_directory = os.getcwd()
myShellScripts = os.environ.get('MY_SHELL_SCRIPTS', present_directory)

# Remove all .sh files, mySetup.txt, and library dir from home
def safe_unlink(path):
    try:
        if os.path.islink(path) or os.path.isfile(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    except Exception:
        pass

for pattern in ['*.sh', 'mySetup.txt']:
    for f in glob.glob(os.path.join(home, pattern)):
        safe_unlink(f)
safe_unlink(os.path.join(home, 'library'))

# Remove backup files (*.*~) from myShellScripts
def remove_backups(directory):
    for f in glob.glob(os.path.join(directory, '*.*~')):
        os.remove(f)

if os.path.isdir(myShellScripts):
    remove_backups(myShellScripts)

# Make all .sh files in myShellScripts executable
for f in glob.glob(os.path.join(myShellScripts, '*.sh')):
    st = os.stat(f)
    os.chmod(f, st.st_mode | stat.S_IEXEC)

# Create symlinks for all .sh files, mySetup.txt, and library dir in home
def symlink_force(target, link_name):
    try:
        if os.path.lexists(link_name):
            os.unlink(link_name)
    except Exception:
        pass
    os.symlink(target, link_name)

for f in glob.glob(os.path.join(myShellScripts, '*.sh')):
    symlink_force(f, os.path.join(home, os.path.basename(f)))

mySetup = os.path.join(myShellScripts, 'mySetup.txt')
if os.path.exists(mySetup):
    symlink_force(mySetup, os.path.join(home, 'mySetup.txt'))

library_dir = os.path.join(myShellScripts, 'library')
if os.path.exists(library_dir):
    symlink_force(library_dir, os.path.join(home, 'library')) 