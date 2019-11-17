import wget, zipfile
from scripts.checkforinternetconnection import check_internet_connection
from globals import *
from version import *
from scripts.install_bar import *

def check_for_upgrade():
    print("Checking for upgrade ... ", end='')
    if check_internet_connection():
        if os.path.isfile(currentdir + "newestversion.txt"):
            os.remove(currentdir + "newestversion.txt")
        wget.download("https://raw.githubusercontent.com/Zorz42/jpm/master/jpm-sources/version.py", currentdir + "newestversion.txt", bar=empty_bar)
    with open(currentdir + "newestversion.txt") as newest_version:
        newestversion = newest_version.read().split()[2]
        newestversion = newestversion[1:len(newestversion)-1]
        print("DONE")
        if newestversion != version:
            return True
        else:
            return False

def forceupgrade():
    print("\x1b[0mDownloading jpm:")
    if os.path.isfile(currentdir + "newerjpm.zip"):
        os.remove(currentdir + "newerjpm.zip")
    wget.download("https://github.com/Zorz42/jpm/archive/master.zip", currentdir + "newerjpm.zip", bar=install_bar)
    print("Extracting jpm ... ", end='')
    with zipfile.ZipFile(currentdir + "newerjpm.zip", 'r') as zip_ref:
        zip_ref.extractall(currentdir)
    print("DONE")
    print("Installing jpm:")
    os.system("cd jpm-master && python3 install.py dependencies && python3 install.py install")


def upgrade():
    if not check_for_upgrade():
        print("\x1b[0mJPM is up to date.")
        return
    forceupgrade()