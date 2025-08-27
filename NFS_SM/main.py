from headers import Utils, ini
import os
from enum import Enum
import shutil

found = False
running = True

class selectedaction(Enum):
    Nul = 0
    Delete = 1
    Backup = 2 

selectedactionint = selectedaction.Nul

def applyselectedaction(path):
    if selectedactionint == selectedaction.Backup:
        shutil.copyfile(path, path + ".bak")
    elif selectedactionint == selectedaction.Delete:
        os.remove(path)

    return

usagetick = 0 # clear at 5 clearing is pretty heavy for the system

def HandleInput(input):
    _input = 0
    invalid = True
    global running, selectedactionint # i hate python why cant everything be global by default

    if type(input) != int:
        print("invalid input")
        return
    
    if input == 1:
        Utils.search4saves()
        return
    elif input == 2:
        if not Utils.saves:
            print("empty....")
            return
        for i, save in enumerate(Utils.saves):
            print(f"{i}. {save}")
        return
    elif input == 3:
        if not Utils.saves:
            print("empty....")
            return
        for i, save in enumerate(Utils.saves):
            print(f"{i}. {save}")

        while invalid:
            try:
                _input = int(input("select an option >> "))
                invalid = False
            except ValueError:
                print("invalid input")
            
        selectedactionint = selectedaction.Backup
        applyselectedaction(Utils.saves[_input])
        return
    elif input == 4:
        if not Utils.saves:
            print("empty....")
            return
        for i, save in enumerate(Utils.saves):
            print(f"{i}. {save}")

        while invalid:
            try:
                _input = int(input("select an option >> "))
                invalid = False
            except ValueError:
                print("invalid input")
            
        selectedactionint = selectedaction.Delete
        applyselectedaction(Utils.saves[_input])
        return
    elif input == 5:
        running = False
        return

    return

def menu():
    global _input
    print("1 - search for save files")
    print("2 - list save files")
    print("3 - backup save file")
    print("4 - delete save file")
    print("5 - exit")

    try:
        _input = int(input("select an option >> "))
    except ValueError:
        print("invalid input")
        return

    
    HandleInput(_input)

    return

def main():
    global usagetick,selectedactionint
    found = os.path.isfile(ini.filename)

    print(
        "\nNFS_SFM\nneed for speed save file manager\nver 0.1\n"
        )

#Utils.search4saves
    if found:
        print("config.ini was found")
    else:
        print("no config.ini was found")

    while running:
        if usagetick > 9:
            Utils.clearconsole()
        menu()
        usagetick = usagetick + 1
        selectedactionint = selectedaction.Nul

main()