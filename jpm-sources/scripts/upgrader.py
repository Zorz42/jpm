import shutil
import wget
import zipfile

from globals import *
from scripts.checkforinternetconnection import check_internet_connection
from scripts.install_bar import *
from version import *
from globals import *

newestversion = None

def check_for_upgrade():
    print_debug("Checking for upgrade ... ", end='')
    if is_internet_connection:
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


def forceupgrade(version="master"):
    print_normal("Downloading jpm:")
    if os.path.isfile(currentdir + "newerjpm.zip"):
        os.remove(currentdir + "newerjpm.zip")
    try:
        wget.download("https://github.com/Zorz42/jpm/archive/" + str(version) +".zip", currentdir + "newerjpm.zip", bar=install_bar)
    except:
        print_error("Non-existent version was prompted to install.")
        exit(0)
    if version[0] == 'v':
        version = version[1:]
    print_debug("\nExtracting jpm ... ", end='')
    with zipfile.ZipFile(currentdir + "newerjpm.zip", 'r') as zip_ref:
        zip_ref.extractall(currentdir)
    print_normal("DONE")
    print_normal("Installing jpm...")
    os.system("cd " + currentdir + "jpm-" + str(version) + " && python3 install.py dependencies && python3 install.py install")
    print_debug("Cleaning up ... ", end='')
    os.remove(currentdir + "newerjpm.zip")
    shutil.rmtree(currentdir + "jpm-" + str(version))
    print_debug("DONE")


def upgrade():
    if not check_for_upgrade():
        print_normal("JPM is up to date.")
        return
    forceupgrade("v" + newestversion)
