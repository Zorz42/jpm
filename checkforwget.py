from install import decision
from os import system
from pkgutil import iter_modules


def check_for_package(name):
    print("PIP3-" + name.upper() + " ... ", end='', flush=True)
    if name in (name for loader, name, ispkg in iter_modules()):
        print("OK")
    else:
        print("FAILED")
        if decision("Do you want me to install python3-" + name + "?"):
            system("pip3 install " + name)
        else:
            exit(1)


check_for_package("wget")
check_for_package("zipfile")
check_for_package("bs4")
