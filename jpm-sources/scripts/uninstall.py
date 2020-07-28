from os import remove
from shutil import rmtree

from globals import choice


def uninstall():
    print("By running this you will uninstall all jac related software on this computer!")
    if choice():
        print("Removing jac software.")
        remove("/usr/local/bin/jaclang")
        rmtree("/usr/local/share/jaclang-data")
        rmtree("/usr/local/share/jaclang-libraries")

        remove("/usr/local/bin/jpm")
        rmtree("/usr/local/share/jpm-sources")

        remove("/usr/local/bin/jacmake")
        rmtree("/usr/local/share/jacmake-sources")

        print("Jac software removed!")
