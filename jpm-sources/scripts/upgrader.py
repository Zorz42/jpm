from os import path, remove, system
from shutil import rmtree
from subprocess import check_output
from zipfile import ZipFile

from wget import download

from globals import print_debug, print_normal, currentdir, datadir
from scripts.checkforinternetconnection import check_internet_connection
from scripts.cleanup import cleanup
from scripts.install_bar import install_bar

newest_jaclang_version = ""

install_directory = "/usr/local/share/"


def check_for_jaclang_upgrade():
    print_debug("Checking for jaclang upgrade ... ", end='', flush=True)
    if check_internet_connection():
        if path.isfile(datadir + "newestjaclangversion.txt"):
            remove(datadir + "newestjaclangversion.txt")
        download("https://raw.githubusercontent.com/Zorz42/jaclang/master/include/version.h", datadir +
                 "newestjaclangversion.txt", bar=None)
    else:
        print("Could not establish internet connection!")
    with open(datadir + "newestjaclangversion.txt") as newest_version:
        global newest_jaclang_version
        newest_jaclang_version = [line.split(" ")[2] for line in newest_version.read().split("\n")
                                  if len(line.split(" ")) == 3]
        newest_jaclang_version = [i[1:len(i) - 1] for i in newest_jaclang_version]
        newest_jaclang_version = "BETA " + ".".join(newest_jaclang_version)
        try:
            currentjaclangversion = check_output(["jaclang", "--version"])
        except FileNotFoundError:
            currentjaclangversion = b"nonexistent"
        currentjaclangversion = currentjaclangversion[:len(currentjaclangversion) - 1]
        currentjaclangversion = currentjaclangversion.decode("utf-8")
        print_debug("DONE")
        return str(newest_jaclang_version) != str(currentjaclangversion)


def upgrade_jaclang():
    newest_jaclang_version_processed = "beta-" + newest_jaclang_version.split(" ")[1]
    print_normal("Downloading jaclang:")
    if path.isfile(currentdir + "newerjaclang.zip"):
        remove(currentdir + "newerjaclang.zip")
    download(f"https://github.com/Zorz42/jaclang/archive/{newest_jaclang_version_processed}.zip",
             currentdir + "newerjaclang.zip", bar=install_bar)

    print_normal("\nExtracting jaclang ... ", end='', flush=True)
    with ZipFile(currentdir + "newerjaclang.zip", 'r') as zip_ref:
        zip_ref.extractall(currentdir)
    print_normal("DONE")
    print_normal("Installing jaclang...")
    system(f"cd {currentdir}jaclang-{newest_jaclang_version_processed} && make")
    print_normal()

    print_debug("Cleaning up ... ", end='', flush=True)
    remove(currentdir + "newerjaclang.zip")
    rmtree(currentdir + f"jaclang-{newest_jaclang_version_processed}")
    print_debug("DONE")
    cleanup()


def upgrade():
    if not check_for_jaclang_upgrade():
        print_normal("Jaclang is up to date.")
    else:
        upgrade_jaclang()


def check_for_jpm_update():
    if check_for_jaclang_upgrade():
        print_normal("Jaclang needs to be updated! Update it by typing jpm upgrade!")
        print_debug(end='')
    else:
        print_debug("Jaclang is up to date.")
