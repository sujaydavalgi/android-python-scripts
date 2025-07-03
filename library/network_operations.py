import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import android_scripts_python.library.log_functions as log_functions
import subprocess
from typing import Optional

def build_ip_address(device_serial: str):
    is_wifi_up = False
    is_wifi_ip = False
    wifi_ip = "0.0.0.0"
    wifi_port = None
    is_eth_up = False
    is_eth_ip = False
    eth_ip = "0.0.0.0"
    eth_port = None
    try:
        result = subprocess.run([
            "adb", "-s", device_serial, "wait-for-device", "shell", "netcfg"
        ], stdout=subprocess.PIPE, text=True)
        for line in result.stdout.strip().split('\n'):
            parts = line.split()
            if len(parts) < 3:
                continue
            interface, up_down, ip_port = parts[0], parts[1], parts[2]
            ip_address = ip_port.split('/')[0]
            ip_port_num = ip_port.split('/')[1] if '/' in ip_port else None
            if interface == "wlan0":
                if up_down == "UP":
                    is_wifi_up = True
                elif up_down == "DOWN":
                    is_wifi_up = False
                if ip_address not in ["0.0.0.0", "127.0.0.1"]:
                    is_wifi_ip = True
                    wifi_ip = ip_address
                    wifi_port = ip_port_num
            if interface == "eth0":
                if up_down == "UP":
                    is_eth_up = True
                elif up_down == "DOWN":
                    is_eth_up = False
                if ip_address not in ["0.0.0.0", "127.0.0.1"]:
                    is_eth_ip = True
                    eth_ip = ip_address
                    eth_port = ip_port_num
    except Exception as e:
        log_functions.write_to_logs_file(f"Error building IP address: {e}")
    return {
        'is_wifi_up': is_wifi_up,
        'is_wifi_ip': is_wifi_ip,
        'wifi_ip': wifi_ip,
        'wifi_port': wifi_port,
        'is_eth_up': is_eth_up,
        'is_eth_ip': is_eth_ip,
        'eth_ip': eth_ip,
        'eth_port': eth_port
    }

def check_wifi(ip_info: dict) -> bool:
    return ip_info['is_wifi_ip'] and ip_info['is_wifi_up']

def check_eth(ip_info: dict) -> bool:
    return ip_info['is_eth_ip'] and ip_info['is_eth_up']

def check_eth_wifi(device_serial: str) -> str:
    ip_info = build_ip_address(device_serial)
    wifi = check_wifi(ip_info)
    eth = check_eth(ip_info)
    if wifi and eth:
        return "Both"
    elif wifi and not eth:
        return "WiFi"
    elif not wifi and eth:
        return "Ethernet"
    else:
        return "None"

def get_my_ip(device_serial: str) -> str:
    ip_info = build_ip_address(device_serial)
    conn_type = check_eth_wifi(device_serial)
    if conn_type == "Both":
        return ip_info['eth_ip']
    elif conn_type == "WiFi":
        return ip_info['wifi_ip']
    elif conn_type == "Ethernet":
        return ip_info['eth_ip']
    else:
        return "None"

def get_device_ip(device_serial: str) -> str:
    try:
        result = subprocess.run([
            "adb", "-s", device_serial, "wait-for-device", "shell", "ip", "route"
        ], stdout=subprocess.PIPE, text=True)
        for line in result.stdout.strip().split('\n'):
            parts = line.split()
            if len(parts) >= 9:
                return parts[8]
    except Exception as e:
        log_functions.write_to_logs_file(f"Error getting device IP: {e}")
    return ""

def get_device_wifi_interface(device_serial: str) -> str:
    try:
        result = subprocess.run([
            "adb", "-s", device_serial, "wait-for-device", "shell","getprop", "wifi.interface"], stdout=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except Exception as e:
        log_functions.write_to_logs_file(f"Error getting device WiFi interface: {e}")
        return "" 