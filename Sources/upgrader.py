from os import remove, system, popen, stat, path
from shutil import rmtree
from tarfile import open as tar_open
from time import time

from globals import jacdir, cachedir, makeCacheDir
from checkForRepositoryConnection import checkRepConnection
from util import downloadFile, extractTar

newest_version: str


def checkForJaclangUpgrade(check_anyways=False):
    makeCacheDir()
    # download jaclang version file if could connect to the internet

    # check if it is internet connection and if newestversion.txt was not updated in the last 24 hours
    if check_anyways or (not path.isfile(f"{cachedir}newestversion.txt") or
                         time() - stat(f"{cachedir}newestversion.txt").st_ctime >= 86400 and checkRepConnection()):
        downloadFile("https://raw.githubusercontent.com/Zorz42/jaclang/master/Headers/version.h",
                     f"{cachedir}newestversion.txt")

    # open version file
    with open(f"{cachedir}newestversion.txt") as newest_version_file:
        global newest_version
        # parse version file
        newest_version = "BETA " + ".".join([line.split(" ")[2][1:-1] for line in
                                             newest_version_file.read().split("\n") if line])
        return newest_version != popen(f"{jacdir}Binaries/jaclang --version").read()[:-1]


def upgradeJaclang():
    print("Installing jaclang")

    # download archive
    version = "beta-" + newest_version.split(" ")[1]
    downloadFile(f"https://github.com/Zorz42/jaclang/archive/{version}.tar.gz",
                 f"{cachedir}newerjaclang.tar.gz")

    # extract archive
    extractTar(f"{cachedir}newerjaclang.tar.gz", cachedir)

    # install jaclang
    system(f"make -C {cachedir}jaclang-{version}")

    # cleanup
    remove(f"{cachedir}newerjaclang.tar.gz")
    rmtree(f"{cachedir}jaclang-{version}")


def upgrade():
    if checkForJaclangUpgrade(check_anyways=True):
        upgradeJaclang()
    else:
        print("Jaclang is up to date.")


def checkForJaclangUpdate():
    if checkForJaclangUpgrade():
        print("Jaclang needs to be updated! Update it by typing jpm upgrade!")
