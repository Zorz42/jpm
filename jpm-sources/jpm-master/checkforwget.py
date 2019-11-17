from install import decision
from os import system

print("PIP3-WGET ... ", end='')

try:
    import wget
    print("OK")
except:
    print("FAILED")
    if decision("Do you want me to install python3-wget?"):
        system("pip3 install wget")
    else:
        exit(1)
