import shutil
import zipfile

import wget

from globals import *
from scripts.checkforinternetconnection import check_internet_connection
from scripts.cleanup import cleanup
from scripts.install_bar import *
from version import *
from urllib import error

newestversion: str


def check_for_upgrade():
    print_debug("Checking for upgrade ... ", end='')
    if check_internet_connection():
        if os.path.isfile(currentdir + "newestversion.txt"):
            os.remove(currentdir + "newestversion.txt")
        wget.download("https://raw.githubusercontent.com/Zorz42/jpm/master/jpm-sources/version.py", currentdir +
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
    if os.path.isfile(currentdir + "newerjpm.zip"):
        os.remove(currentdir + "newerjpm.zip")
    try:
        wget.download("https://github.com/Zorz42/jpm/archive/" + str(version_to_install) + ".zip",
                      currentdir + "newerjpm.zip",
                      bar=install_bar)
    except error.HTTPError:
        print_error("Non-existent version was prompted to install.")
        jpm_exit(0)
    if version_to_install[0] == 'v':
        version_to_install = version_to_install[1:]
    print_normal("\nExtracting jpm ... ", end='')
    with zipfile.ZipFile(currentdir + "newerjpm.zip", 'r') as zip_ref:
        zip_ref.extractall(currentdir)
    print_normal("DONE")
    print_normal("Installing jpm...")
    os.system("cd " + currentdir + "jpm-" + str(
        version_to_install) + " && python3 install.py dependencies && python3 install.py install")
    print_debug("Cleaning up ... ", end='')
    os.remove(currentdir + "newerjpm.zip")
    shutil.rmtree(currentdir + "jpm-" + str(version_to_install))
    print_debug("DONE")
    cleanup()


def upgrade():
    if not check_for_upgrade():
        print_normal("JPM is up to date.")
        return
    forceupgrade("v" + newestversion)
