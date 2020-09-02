from shutil import rmtree
from platform import system as sys
from os import remove

from globals import choice


def uninstall():
    print("By running this you will uninstall all jac related software on this computer!")
    if choice():
        rmtree("/usr/local/Jac")
        remove("/usr/local/bin/jpm")
        remove("/usr/local/bin/jacmake")
        remove("/usr/local/bin/jaclang")
        print("Jac software removed.")
