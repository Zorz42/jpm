from os import system
from globals import *
from getpass import getuser

def repair():
    print_normal("Repairing jpm...")
    system("sudo chmod +rw /usr/local/bin/jpm-sources /usr/local/bin/jpm-sources/* /usr/local/bin/jpm-sources/*/*")
    system("sudo chown " + getuser() +" /usr/local/bin/jpm-sources /usr/local/bin/jpm-sources/* /usr/local/bin/jpm-sources/*/*")
    print_normal("Repair complete!")
