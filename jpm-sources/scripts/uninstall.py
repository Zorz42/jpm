from globals import choice, print_normal, print_debug
from os import system, path
from subprocess import check_output


def list_users():
    return check_output(["cut", "-d:", "-f1", "/etc/passwd"]).decode("utf-8").split("\n")


def get_user_home_dir(user):
    if user == '':
        return "/"
    return check_output(["getent", "passwd", user]).decode("utf-8").split(":")[5]


def uninstall():
    print_normal("By running this you will uninstall all jac related software on this computer!")
    if not choice():
        return
    if path.isfile("/usr/local/bin/jaclang"):
        print_normal("Removing Jaclang")
        system("sudo rm /usr/local/bin/jaclang")

    if path.isfile("/usr/local/bin/jpm"):
        print_normal("Removing JPM")
        system("sudo rm /usr/local/bin/jpm")

    print_normal("Removing other files")

    for user in list_users():
        if path.isdir(get_user_home_dir(user) + "/.local/share/jaclang-data/"):
            print_debug("Removing jaclang files for " + user)
            system("sudo rm -r " + get_user_home_dir(user) + "/.local/share/jaclang-data/")

        if path.isdir(get_user_home_dir(user) + "/.local/share/jpm-sources/"):
            print_debug("Removing jpm-src files for " + user)
            system("sudo rm -r " + get_user_home_dir(user) + "/.local/share/jpm-sources/")
