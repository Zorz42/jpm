from os import path, remove, system
from shutil import rmtree
from urllib import error
from zipfile import ZipFile
from wget import download
from subprocess import check_output

from globals import print_debug, print_normal, print_error, currentdir, jpm_exit
from scripts.checkforinternetconnection import check_internet_connection
from scripts.cleanup import cleanup
from scripts.install_bar import install_bar
from version import version

newestversion = None
newestjaclangversion = None

install_directory = path.expanduser("~") + "/.local/share/"


def check_for_upgrade():
    print_debug("Checking for jpm upgrade ... ", end='', flush=True)
    if check_internet_connection():
        if path.isfile(currentdir + "newestversion.txt"):
            remove(currentdir + "newestversion.txt")
        download("https://raw.githubusercontent.com/Zorz42/jpm/stable/jpm-sources/version.py", currentdir +
                 "newestversion.txt", bar=None)
    with open(currentdir + "newestversion.txt") as newest_version:
        global newestversion
        newestversion = newest_version.read().split()[2]
        newestversion = newestversion[1:len(newestversion) - 1]
        print_debug("DONE")
        return newestversion != version


def check_for_jaclang_upgrade():
    print_debug("Checking for jaclang upgrade ... ", end='', flush=True)
    if check_internet_connection():
        if path.isfile(currentdir + "newestjaclangversion.txt"):
            remove(currentdir + "newestjaclangversion.txt")
        download("https://raw.githubusercontent.com/Zorz42/jaclang/stable/include/version.h", currentdir +
                 "newestjaclangversion.txt", bar=None)
    with open(currentdir + "newestjaclangversion.txt") as newest_version:
        global newestjaclangversion
        newestjaclangversion = [line.split(" ")[2] for line in newest_version.read().split("\n")
                                if len(line.split(" ")) == 3]
        newestjaclangversion = [i[1:len(i) - 1] for i in newestjaclangversion]
        newestjaclangversion = "BETA " + ".".join(newestjaclangversion)
        try:
            currentjaclangversion = check_output(["jaclang", "--version"])
        except FileNotFoundError:
            currentjaclangversion = b"nonexistent"
        currentjaclangversion = currentjaclangversion[:len(currentjaclangversion) - 1]
        currentjaclangversion = currentjaclangversion.decode("utf-8")
        print_debug("DONE")
        return str(newestjaclangversion) != str(currentjaclangversion)


def upgrade_jpm():
    print_normal("Downloading jpm:")
    if path.isfile(currentdir + "newerjpm.zip"):
        remove(currentdir + "newerjpm.zip")
    download("https://github.com/Zorz42/jpm/archive/stable.zip",
             currentdir + "newerjpm.zip",
             bar=install_bar)
    print_normal("\nExtracting jpm ... ", end='', flush=True)
    with ZipFile(currentdir + "newerjpm.zip", 'r') as zip_ref:
        zip_ref.extractall(currentdir)
    print_normal("DONE")
    print_normal("Installing jpm...")
    system("cd " + currentdir + "jpm-stable && cp -r jpm-sources " + install_directory)

    print_debug("Cleaning up ... ", end='', flush=True)
    remove(currentdir + "newerjpm.zip")
    rmtree(currentdir + "jpm-stable")
    print_debug("DONE")
    cleanup()


def upgrade_jaclang():
    print_normal("Downloading jaclang:")
    if path.isfile(currentdir + "newerjaclang.zip"):
        remove(currentdir + "newerjaclang.zip")
    download("https://github.com/Zorz42/jaclang/archive/stable.zip",
             currentdir + "newerjaclang.zip",
             bar=install_bar)

    print_normal("\nExtracting jpm ... ", end='', flush=True)
    with ZipFile(currentdir + "newerjaclang.zip", 'r') as zip_ref:
        zip_ref.extractall(currentdir)
    print_normal("DONE")
    print_normal("Installing jaclang...")
    system("cd " + currentdir + "jaclang-stable && make onlyjaclang")
    print_normal()

    print_debug("Cleaning up ... ", end='', flush=True)
    remove(currentdir + "newerjaclang.zip")
    rmtree(currentdir + "jaclang-stable")
    print_debug("DONE")
    cleanup()


def upgrade():
    if not check_for_upgrade():
        print_normal("JPM is up to date.")
    else:
        upgrade_jpm()
    if not check_for_jaclang_upgrade():
        print_normal("Jaclang is up to date.")
    else:
        upgrade_jaclang()


# check or jpm update (upgrade)
def check_for_jpm_update():
    if check_for_upgrade():
        print_normal("JPM needs to be updated! Update it by typing jpm upgrade!")
        print_debug(end='')
    else:
        print_debug("JPM is up to date.")
    if check_for_jaclang_upgrade():
        print_normal("Jaclang needs to be updated! Update it by typing jpm upgrade!")
        print_debug(end='')
    else:
        print_debug("Jaclang is up to date.")
