from os import remove, system, popen
from shutil import rmtree
from tarfile import open as tar_open
from time import time
from os import stat

from globals import currentdir, datadir, removeFileIfExists, downloadFile, jacdir
from scripts.checkForRepositoryConnection import checkRepConnection

newest_version: str


def checkForJaclangUpgrade(check_anyways=False):
    # download jaclang version file if could connect to the internet

    # check if it is internet connection and if newestversion.txt was not updated in the last 24 hours
    if check_anyways or (checkRepConnection() and
                         (time() - stat(f"{datadir}newestversion.txt").st_ctime >= 86400 or
                          open(f"{datadir}newestversion.txt").read() != "nonexistent\n")):
        downloadFile("https://raw.githubusercontent.com/Zorz42/jaclang/master/Headers/version.h",
                     f"{datadir}newestversion.txt")

    # open version file
    with open(datadir + "newestversion.txt") as newest_version_file:
        global newest_version
        # parse version file
        newest_version = "BETA " + ".".join([line.split(" ")[2][1:-1] for line in
                                             newest_version_file.read().split("\n") if line])
        try:
            currentjaclangversion = popen(f"{jacdir}Binaries/jaclang --version").read()[:-1]
        except FileNotFoundError:
            currentjaclangversion = b"nonexistent"

        return newest_version != currentjaclangversion


def upgradeJaclang():
    print("Installing jaclang")

    # download archive
    version = "beta-" + newest_version.split(" ")[1]
    removeFileIfExists(f"{currentdir}newerjaclang.zip")
    downloadFile(f"https://github.com/Zorz42/jaclang/archive/{version}.tar.gz",
                 f"{currentdir}newerjaclang.tar.gz")

    # extract archive
    with tar_open(f"{currentdir}newerjaclang.tar.gz", "r:gz") as tar_file:
        tar_file.extractall(path=currentdir)

    # install jaclang
    system(f"make -C {currentdir}jaclang-{version}")

    # cleanup
    remove(f"{currentdir}newerjaclang.zip")
    rmtree(f"{currentdir}jaclang-{version}")


def upgrade():
    if checkForJaclangUpgrade(check_anyways=True):
        upgradeJaclang()
    else:
        print("Jaclang is up to date.")


def checkForJaclangUpdate():
    if checkForJaclangUpgrade():
        print("Jaclang needs to be updated! Update it by typing jpm upgrade!")
