from os import remove
from shutil import rmtree

from globals import choice, print_normal


def uninstall():
    print_normal("By running this you will uninstall all jac related software on this computer!")
    if not choice():
        return
    print_normal("Removing Jaclang...")
    remove("/usr/local/bin/jaclang")
    rmtree("/usr/local/share/jaclang-data")

    print_normal("Removing JPM...")
    remove("/usr/local/bin/jpm")
    rmtree("/usr/local/share/jpm-sources")

    print_normal("JAC software removed!")
