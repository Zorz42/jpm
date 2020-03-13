from getpass import getuser
from os import system

from globals import print_normal


def repair():
    print_normal("Repairing jpm...")
    system("sudo chmod +rw /usr/local/share/jpm-sources /usr/local/share/jpm-sources/* /usr/local/share/jpm-sources/*/*")
    system(
        "sudo chown " + getuser() + " /usr/local/share/jpm-sources /usr/local/bin/jpm-sources/* "
                                    "/usr/local/share/jpm-sources/*/*")
    system("sudo chmod +rw /usr/local/share/jaclang-data /usr/local/share/jaclang-data/*")
    system(
        "sudo chown " + getuser() + " /usr/local/share/jaclang-data /usr/local/share/jaclang-data/*")
    print_normal("Repair complete!")
