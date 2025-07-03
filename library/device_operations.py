import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import android_scripts_python.library.main_functions as main_functions
from android_scripts_python.library.text_formatting import pbold, format_message

# Device property stubs (to be implemented or imported)
def get_device_name(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "ro.product.device").replace("\r", "").replace("\n", "")

def get_device_build(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "ro.build.display.id").replace("\r", "").replace("\n", "")

def get_device_model(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "ro.product.model").replace("\r", "").replace("\n", "")

def get_device_keys(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "ro.build.tags").replace("\r", "").replace("\n", "")

def get_device_build_version(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "ro.build.version.release").replace("\r", "").replace("\n", "")

def get_device_manufacturer(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "ro.product.manufacturer").replace("\r", "").replace("\n", "")

def get_device_build_type(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "ro.build.type").replace("\r", "").replace("\n", "")

def get_device_encrypt_state(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "ro.crypto.state").replace("\r", "").replace("\n", "")

def get_device_boot_complete_state(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "sys.boot_completed").replace("\r", "").replace("\n", "")

def get_device_boot_animation_state(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "init.svc.bootanim").replace("\r", "").replace("\n", "")

def get_device_sim_status(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell", "getprop", "gsm.sim.state").replace("\r", "").replace("\n", "")

def get_device_type(device_serial: str) -> str:
    # Heuristics based on device properties
    model = get_device_model(device_serial).lower()
    name = get_device_name(device_serial).lower()
    # build = get_device_build(device_serial).lower()
    brand = get_product_brand(device_serial).lower()

    # Watch
    if any(x in model for x in ["watch", "wear"]) or any(x in name for x in ["watch", "wear"]):
        return "watch"
    # TV
    if any(x in model for x in ["tv", "bravia", "shield"]) or any(x in name for x in ["tv", "bravia", "shield"]):
        return "tv"
    # Auto
    if any(x in model for x in ["car", "auto"]) or any(x in name for x in ["car", "auto"]):
        return "auto"
    # Things (IoT)
    if any(x in model for x in ["things", "iot"]) or any(x in name for x in ["things", "iot"]):
        return "things"
    # Tablet
    if any(x in model for x in ["tablet", "pad"]) or any(x in name for x in ["tablet", "pad"]):
        return "tablet"
    # Phone (default for common brands/models)
    if any(x in brand for x in ["google", "samsung", "oneplus", "xiaomi", "oppo", "vivo", "realme", "motorola", "sony", "nokia", "huawei", "asus", "lenovo"]):
        if not ("tv" in model or "watch" in model or "auto" in model or "things" in model or "tablet" in model):
            return "phone"
    # Fallback
    return "default"

def get_product_brand(device_serial: str) -> str:
    return main_functions.adb_shell(device_serial, "shell","getprop", "ro.product.brand").replace("\r", "").replace("\n", "")

# Utility

def display_selected_device(device_serial: str):
    print("Selected device : ", end='')
    pbold(device_serial)
    print()  # Newline after serial
    if is_device_offline(device_serial) or is_device_unauthorized(device_serial):
        format_message(" - Device is offline/Unauthorised. Cannot do anything with it\n\n", "E")
        return
    if is_adb_device(device_serial):
        device_name = get_device_name(device_serial)
        device_build = get_device_build(device_serial)
        device_model = get_device_model(device_serial)
        device_keys = get_device_keys(device_serial)
        device_build_version = get_device_build_version(device_serial)
        device_manufacturer = get_device_manufacturer(device_serial)
        info_msg = f"{device_manufacturer} {device_model} - {device_build_version} {device_build} ({device_name} {device_keys})"
        if info_msg.strip():
            format_message(info_msg, "I")
            print()
    # Print date/time if needed

# Example: compare build versions (float comparison)
def compare_device_build_version(device_serial: str, compare_with_version: str) -> str:
    device_build_version = get_device_build_version(device_serial)
    try:
        v1 = float(device_build_version)
        v2 = float(compare_with_version)
        if v1 > v2:
            return "greater"
        elif v1 < v2:
            return "smaller"
        else:
            return "same"
    except Exception:
        return "unknown"

def is_device_build_userdebug(device_serial: str) -> bool:
    return get_device_build_type(device_serial) == "userdebug"

def is_device_build_user(device_serial: str) -> bool:
    return get_device_build_type(device_serial) == "user"

def is_device_build_release_key(device_serial: str) -> bool:
    return get_device_keys(device_serial) == "release-keys"

def is_device_build_dev_key(device_serial: str) -> bool:
    return get_device_keys(device_serial) == "dev-keys"

def is_device_build_test_key(device_serial: str) -> bool:
    return get_device_keys(device_serial) == "test-keys"

def is_device_encrypted(device_serial: str) -> bool:
    return get_device_encrypt_state(device_serial) == "encrypted"

def is_device_boot_complete(device_serial: str) -> bool:
    return get_device_boot_complete_state(device_serial) == "1"

def is_device_boot_animation_complete(device_serial: str) -> bool:
    return get_device_boot_animation_state(device_serial) == "stopped"

def is_device_sim_ready(device_serial: str) -> bool:
    return get_device_sim_status(device_serial) == "READY"

def is_device_default(device_serial: str) -> bool:
    return get_device_type(device_serial) == "default"

def is_device_no_sdcard(device_serial: str) -> bool:
    return get_device_type(device_serial) == "nosdcard"

def is_device_phone(device_serial: str) -> bool:
    return get_device_type(device_serial) == "phone"

def is_device_tablet(device_serial: str) -> bool:
    return get_device_type(device_serial) == "tablet"

def is_device_tv(device_serial: str) -> bool:
    return get_device_type(device_serial) == "tv"

def is_device_wear(device_serial: str) -> bool:
    return get_device_type(device_serial) == "watch"

def is_device_auto(device_serial: str) -> bool:
    return get_device_type(device_serial) == "auto"

def is_device_things(device_serial: str) -> bool:
    return get_device_type(device_serial) == "things"

def is_at_home_device(device_serial: str) -> bool:
    return get_device_name(device_serial) in ["tungsten", "cujo", "wolfie", "molly", "fugu"]

def is_clockwork_device(device_serial: str) -> bool:
    return get_device_name(device_serial) in ["sprat", "dorry", "minnow"]

def is_gearhead_device(device_serial: str) -> bool:
    # Not yet implemented
    return False

def is_ged_device(device_serial: str) -> bool:
    if get_product_brand(device_serial) == "google":
        return True
    return get_device_name(device_serial) in [
        "prime", "hammerhead", "mako", "nakasi", "nakasig", "flo", "deb", "manta", "mantaray", "shamu", "razor", "razorg", "volantis", "volantisg", "angler", "bullhead"
    ]

def is_gpe_device(device_serial: str) -> bool:
    return get_device_name(device_serial) in ["jgedlteue", "-blablabla-", "ghost_retail"]

def is_google_device(device_serial: str) -> bool:
    return (
        is_at_home_device(device_serial)
        or is_clockwork_device(device_serial)
        or is_ged_device(device_serial)
    )

def is_adb_device(device_serial: str) -> bool:
    idx = get_index(device_serial)
    return main_functions.DEVICE_ARRAY_STATUS[idx] == "adb"

def is_recovery_device(device_serial: str) -> bool:
    idx = get_index(device_serial)
    return main_functions.DEVICE_ARRAY_STATUS[idx] == "recovery"

def is_fastboot_device(device_serial: str) -> bool:
    idx = get_index(device_serial)
    return main_functions.DEVICE_ARRAY_STATUS[idx] == "fastboot"

def is_device_offline(device_serial: str) -> bool:
    idx = get_index(device_serial)
    return main_functions.DEVICE_ARRAY_STATUS[idx] == "offline"

def is_device_unauthorized(device_serial: str) -> bool:
    idx = get_index(device_serial)
    return main_functions.DEVICE_ARRAY_STATUS[idx] == "unauthorized"

def get_index(device_serial: str) -> int:
    try:
        serials = [s.strip() for s in main_functions.DEVICE_ARRAY]
        idx = serials.index(device_serial.strip())
        return idx
    except ValueError:
        format_message("\n Lost the Device OR Device not Found\n", "E")
        print("DEVICE_ARRAY:", main_functions.DEVICE_ARRAY)
        print("Selected deviceSerial:", device_serial)
        raise 