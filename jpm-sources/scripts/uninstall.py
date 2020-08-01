from shutil import rmtree

from globals import choice


def uninstall():
    print("By running this you will uninstall all jac related software on this computer!")
    if choice():
        rmtree("/usr/local/Jac")
        print("Jac software removed.")