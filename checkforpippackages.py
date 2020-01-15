from install import decision
from os import system
from pkgutil import iter_modules

packages = [name for loader, name, ispkg in iter_modules()]

def check_for_package(name):
    print("PIP3-" + name.upper() + " ... ", end='', flush=True)
    if name in packages:
        print("OK")
    else:
        print("FAILED")
        if decision("Do you want me to install python3-" + name + "?"):
            system("pip3 install " + name)
        else:
            exit(1)

needed_packages = (
    "wget",
    "zipfile",
    "bs4"
)

def checkforpippackages_main():
    for package in needed_packages:
        check_for_package(package)
