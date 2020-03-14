from getpass import getuser
from os import system, path

from globals import print_normal

install_directory = path.expanduser("~") + "/.local/share/"


def repair():
    print_normal("Repairing jpm...")
    system("sudo chmod +rw " + install_directory + "/jpm-sources " + install_directory + "jpm-sources/* " +
           install_directory + "jpm-sources/*/*")
    system(
        "sudo chown " + getuser() + " " + install_directory + "jpm-sources " + install_directory + "jpm-sources/* " +
        install_directory + "jpm-sources/*/*")
    system("sudo chmod +rw ~/.local/share/jaclang-data ~/.local/share/jaclang-data/*")
    system(
        "sudo chown " + getuser() + " " + install_directory + "/jaclang-data " + install_directory + "jaclang-data/*")
    print_normal("Repair complete!")
