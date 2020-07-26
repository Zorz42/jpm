from os import remove
from shutil import rmtree

from globals import choice


def uninstall():
    print("By running this you will uninstall all jac related software on this computer!")
    if not choice():
        return
    print("Removing Jaclang...")
    remove("/usr/local/bin/jaclang")
    rmtree("/usr/local/share/jaclang-data")

    print("Removing JPM...")
    remove("/usr/local/bin/jpm")
    rmtree("/usr/local/share/jpm-sources")

    print("JAC software removed!")
