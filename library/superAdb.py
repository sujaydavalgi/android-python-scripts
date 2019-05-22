#! /usr/bin/env python

import subprocess
import tempfile
import urllib
import sys

def echo(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()

def call(cmd):
    try:
        return subprocess.check_output('adb -s %s %s' % (call.device, cmd), shell=True)
    except Exception as e:
        return e.output

def _get_devices():
    try:
        devices = subprocess.check_output('adb devices', shell=True)
    except:
        return None
    devices = devices.strip().split('\n')
    devices = devices[1:]
    return [line.split()[0] for line in devices]

def select_device():
    devices = _get_devices()
    if not devices:
        sys.exit('No devices found, Have you connect to any devices?')
    length = len(devices)
    if length > 1:
        echo('multiple devices found:\n')
        for index, d in enumerate(devices):
            echo('%s. %s\n' % (index, d))
        select = raw_input('Select (0~%s):\n' % (length - 1))
        while (select.strip() not in [str(i) for i in range(length)]):
            select = raw_input('Please enter the number 0~%s:\n' % (length - 1))
        return devices[int(select)]
    else:
        return devices[0]
            
def detect_busybox():
    output = call('shell ls -al /data/local/tmp/busybox')
    if not output:
        return False
    output = output.lower()
    if "no such file" in output:
        return False
    permission = output.split()[0]
    if permission.endswith('x'):
        return True
    else:
        # no permission
        permission_ret = call('shell chmod +x /data/local/tmp/busybox')
        if not permission_ret:
            return True
        return False

def install():
    def report(count, size, total):
        percent = int(count * size * 100 / total)
        sys.stdout.write("\r %d%%" % percent + ' complete')
        sys.stdout.flush()

    binary = tempfile.NamedTemporaryFile()
    echo("download busybox binary...\n")
    urllib.urlretrieve('https://github.com/tiann/super-adb/raw/master/busybox-armv6l', binary.name, reporthook=report)
    out = call('push %s /data/local/tmp/busybox' % binary.name)
    if "error" in out.lower():
        raise Error('push busybox failed.')
    out = call('shell chmod 777 /data/local/tmp/busybox')
    echo('change permission : %s\n' % out)
    out = call('shell /data/local/tmp/busybox --install -s /data/local/tmp/')
    echo("install busybox : %s\n" % out)

def interact():
    try:
        pexpect = __import__('pexpect')
    except ImportError:
        raise Exception('Please install the pexpect module first!! \nYou can do it by "pip install pexpect"')
    shell = pexpect.spawn('adb -s %s shell' % call.device)
    shell.expect('$')
    shell.sendline('export PATH=/data/local/tmp/:$PATH')
    shell.sendline('clear')
    shell.interact()

def main():
    call.device = select_device()
    if not detect_busybox():
        echo("install busybox...\n")
        install()
    interact()

if __name__ == '__main__':
    main()
