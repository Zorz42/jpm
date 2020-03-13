from getpass import getuser
from os import system

from globals import print_normal


def repair():
    print_normal("Repairing jpm...")
    system("sudo chmod +rw ~/.local/share/jpm-sources ~/.local/share/jpm-sources/* ~/.local/share/jpm-sources/*/*")
    system(
        "sudo chown " + getuser() + " ~/.local/share/jpm-sources ~/.local/share/jpm-sources/* "
                                    "~/.local/share/jpm-sources/*/*")
    system("sudo chmod +rw ~/.local/share/jaclang-data ~/.local/share/jaclang-data/*")
    system(
        "sudo chown " + getuser() + " ~/.local/share/jaclang-data ~/.local/share/jaclang-data/*")
    print_normal("Repair complete!")
