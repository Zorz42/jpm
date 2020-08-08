from shutil import rmtree
from platform import system as sys
from os import remove

from globals import choice


def uninstall():
    print("By running this you will uninstall all jac related software on this computer!")
    if choice():
        rmtree("/usr/local/Jac")
        remove("/etc/profile.d/jaclang-paths.sh" if sys() == "Linux" else "/etc/paths.d/jaclang-paths")
        print("Jac software removed.")
