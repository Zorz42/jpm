from os import path, remove, system
from shutil import rmtree
from urllib import error
from zipfile import ZipFile

from wget import download

from globals import print_debug, print_normal, print_error, currentdir, jpm_exit
from scripts.checkforinternetconnection import check_internet_connection
from scripts.cleanup import cleanup
from scripts.install_bar import install_bar
from version import version

newestversion = None


def check_for_upgrade():
    print_debug("Checking for upgrade ... ", end='', flush=True)
    if check_internet_connection():
        if path.isfile(currentdir + "newestversion.txt"):
            remove(currentdir + "newestversion.txt")
        download("https://raw.githubusercontent.com/Zorz42/jpm/master/jpm-sources/version.py", currentdir +
                 "newestversion.txt", bar=None)
    with open(currentdir + "newestversion.txt") as newest_version:
        global newestversion
        newestversion = newest_version.read().split()[2]
        newestversion = newestversion[1:len(newestversion) - 1]
        print_debug("DONE")
        if newestversion != version:
            return True
        else:
            return False


def forceupgrade(version_to_install):
    if version_to_install == "vmaster":
        version_to_install = "master"
    print_normal("Downloading jpm:")
    if path.isfile(currentdir + "newerjpm.zip"):
        remove(currentdir + "newerjpm.zip")
    try:
        download("https://github.com/Zorz42/jpm/archive/" + str(version_to_install) + ".zip",
                 currentdir + "newerjpm.zip",
                 bar=install_bar)
    except error.HTTPError:
        print_error("Non-existent version was prompted to install.")
        jpm_exit(0)
    if version_to_install[0] == 'v':
        version_to_install = version_to_install[1:]
    print_normal("\nExtracting jpm ... ", end='', flush=True)
    with ZipFile(currentdir + "newerjpm.zip", 'r') as zip_ref:
        zip_ref.extractall(currentdir)
    print_normal("DONE")
    print_normal("Installing jpm...")
    system("cd " + currentdir + "jpm-" + str(
        version_to_install) + " && cp -r jpm-sources ~/.local/share/")
    print_debug("Cleaning up ... ", end='', flush=True)
    remove(currentdir + "newerjpm.zip")
    rmtree(currentdir + "jpm-" + str(version_to_install))
    print_debug("DONE")
    cleanup()


def upgrade():
    if not check_for_upgrade():
        print_normal("JPM is up to date.")
        return
    forceupgrade("v" + newestversion)


# check or jpm update (upgrade)
def check_for_jpm_update():
    if check_for_upgrade():
        print_normal("JPM needs to be updated! Update it by typing jpm upgrade!")
        print_debug(end='')
    else:
        print_debug("JPM is up to date.")
