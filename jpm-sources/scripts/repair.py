from getpass import getuser
from os import system

from globals import print_normal


def repair():
    print_normal("Repairing jpm...")
    system("sudo chmod +rw /usr/local/bin/jpm-sources /usr/local/bin/jpm-sources/* /usr/local/bin/jpm-sources/*/*")
    system(
        "sudo chown " + getuser() + " /usr/local/bin/jpm-sources /usr/local/bin/jpm-sources/* "
                                    "/usr/local/bin/jpm-sources/*/*")
    system("sudo chmod +rw /usr/local/bin/jaclang-data /usr/local/bin/jaclang-data/*")
    system(
        "sudo chown " + getuser() + " /usr/local/bin/jaclang-data /usr/local/bin/jaclang-data/*")
    print_normal("Repair complete!")
