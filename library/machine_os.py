import platform

def check_my_os_type():
    my_os = platform.system().lower()
    my_kernel = platform.release()
    my_mach = platform.machine()
    my_dist = ''
    my_psuedoname = ''
    my_rev = ''
    my_distro_based_on = ''

    if my_os == 'windows':
        my_os = 'windows'
    elif my_os == 'darwin':
        my_os = 'mac'
    elif my_os == 'linux':
        try:
            import distro
            my_dist = distro.name(pretty=True)
            my_psuedoname = distro.codename()
            my_rev = distro.version()
            my_distro_based_on = distro.like()
        except ImportError:
            # fallback if distro is not installed
            my_dist = ''
            my_psuedoname = ''
            my_rev = ''
            my_distro_based_on = ''
    return {
        'my_os': my_os,
        'my_dist': my_dist,
        'my_psuedoname': my_psuedoname,
        'my_rev': my_rev,
        'my_distro_based_on': my_distro_based_on,
        'my_kernel': my_kernel,
        'my_mach': my_mach
    }

def display_os_type():
    info = check_my_os_type()
    print(f"OS: {info['my_os']}")
    print(f"DIST: {info['my_dist']}")
    print(f"PSUEDONAME: {info['my_psuedoname']}")
    print(f"REV: {info['my_rev']}")
    print(f"DistroBasedOn: {info['my_distro_based_on']}")
    print(f"KERNEL: {info['my_kernel']}")
    print(f"MACH: {info['my_mach']}")

def get_my_os() -> str:
    return check_my_os_type()['my_os']

def get_my_dist() -> str:
    return check_my_os_type()['my_dist']

def get_my_psuedoname() -> str:
    return check_my_os_type()['my_psuedoname']

def get_my_rev() -> str:
    return check_my_os_type()['my_rev']

def get_my_distro_based_on() -> str:
    return check_my_os_type()['my_distro_based_on']

def get_my_kernel() -> str:
    return check_my_os_type()['my_kernel']

def get_my_mach() -> str:
    return check_my_os_type()['my_mach'] 