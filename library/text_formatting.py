def to_lowercase(s: str) -> str:
    return s.lower()

def to_uppercase(s: str) -> str:
    return s.upper()

# ANSI color codes
TXT_RST = '\033[0m'
TXT_BLD = '\033[1m'
TXT_DIM = '\033[2m'
TXT_UND = '\033[4m'
TXT_BLK = '\033[5m'
TXT_REV = '\033[7m'

TXT_BLA = '\033[30m'
TXT_RED = '\033[31m'
TXT_GRN = '\033[32m'
TXT_YLW = '\033[33m'
TXT_BLU = '\033[34m'
TXT_PUR = '\033[35m'
TXT_CYN = '\033[36m'
TXT_WHT = '\033[37m'

BG_RED = '\033[41m'
BG_GRN = '\033[42m'
BG_YLW = '\033[43m'
BG_BLU = '\033[44m'
BG_PUR = '\033[45m'
BG_CYN = '\033[46m'
BG_WHT = '\033[47m'

# Bold print
def pbold(*args, end=''):
    print(f"{TXT_BLD}{' '.join(str(a) for a in args)}{TXT_RST}", end=end)

# Blinking text
def txt_blink(*args, end=''):
    print(f"\033[5m{' '.join(str(a) for a in args)}{TXT_RST}", end=end)

# Example usage of color codes
def color_text(text: str, color: str) -> str:
    return f"{color}{text}{TXT_RST}"

# Example: print(color_text('Hello', TXT_RED)) 

def format_message(msg: str, level: str = None, end: str = "\n"):
    if level == "E":
        print(f"{TXT_RED}{msg}{TXT_RST}", end=end)
    elif level == "W":
        print(f"{TXT_YLW}{msg}{TXT_RST}", end=end)
    elif level == "I":
        print(f"{TXT_GRN}{msg}{TXT_RST}", end=end)
    else:
        print(msg, end=end) 