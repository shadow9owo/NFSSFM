from enum import Enum
import os
from headers import ini
import platform

class ErrorCodes(Enum):
    Success = 0
    Failed = 1
    Unknown_Error = 2
    Access_Error = 3

debug = False # switch this to get spammed :)

# doesnt support rivals because rivals uses .sav which is too common to differentiate it from other games and the save file itself doesnt have a flag which would specify it as a need for speed save file
# wont fix

validationkey_frostbite = b"NFSS" # Unbound , payback , heat , all frostbite games basically
validationkey_blackbox = b"20CMl" # NFSMW2004

validationfilekeyword = ["nfs","save"] # NFSHP 2010 && 2020 && mw 2012

saves = []

#nothing here matters as long as it returns success
def validate_savefile(file):
    try:
        with open(file, "rb") as f:
            header = f.read(len(validationkey_frostbite))  # read first 4 bytes
            if header == validationkey_frostbite:
                return ErrorCodes.Success
            f.seek(0)
            header = f.read(len(validationkey_blackbox))
            if header == validationkey_blackbox:
                return ErrorCodes.Success
            else:
                filename_lower = os.path.basename(file).lower() 
                if any(keyword in filename_lower for keyword in validationfilekeyword):
                    return ErrorCodes.Success
                else:
                    return ErrorCodes.Failed
    except Exception as e:
        if (debug):
            print(f"{e}")
        return ErrorCodes.Access_Error
    
def loadpath():
    global saves
    if os.path.isfile(ini.filename):
        index = 1
        paths = []
        while True:
            key = f"Path{index}"
            value = ini.getvalue(key)
            if value is None:
                break
            paths.append(value)
            index += 1
        saves = paths
    else:
        return
    
def savepath():
    global saves
    if not saves:
        return False

    try:
        with open(ini.filename, "w", encoding="utf-8") as f:
            for index, path in enumerate(saves, start=1):
                f.write(f"Path{index}={path}\n")
        return True
    except Exception as e:
        print(f"{e}")
        return False

def search4saves():
    global saves
    saves = []
    found_set = set()

    cwd = os.getcwd()
    print(f"starting {cwd}")

    os_name = platform.system().lower()
    if os_name == "windows":
        drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
        search_dirs = drives
    else:
        search_dirs = ["/"]

    def onerror(err):
        if debug:
            print(f"Error accessing {getattr(err, 'filename', 'unknown')}: {err}")

    for base_dir in search_dirs:
        print(f"Scanning base: {base_dir}")
        try:
            for root, dirs, files in os.walk(base_dir, onerror=onerror, followlinks=False):
                print(f"scanning: {root}")
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        if validate_savefile(filepath) == ErrorCodes.Success:
                            if filepath not in found_set:
                                found_set.add(filepath)
                                saves.append(filepath)
                                if debug:
                                    print(f"found: {filepath}")
                    except Exception:
                        continue
        except Exception as e:
            if debug:
                print(f"err {base_dir}: {e}")

    return saves

def clearconsole():
    os.system('cls' if os.name == 'nt' else 'clear')
    return
