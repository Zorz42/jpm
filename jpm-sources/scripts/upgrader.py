from os import remove, system
from shutil import rmtree
from subprocess import check_output
from tarfile import open as tar_open

from globals import currentdir, datadir, removeFileIfExists, downloadFile
from scripts.checkForRepositoryConnection import checkRepConnection

newest_version: str


def checkForJaclangUpgrade():
    # download jaclang version file if could connect to the internet
    if checkRepConnection():
        removeFileIfExists(f"{datadir}newestjaclangversion.txt")
        downloadFile("https://raw.githubusercontent.com/Zorz42/jaclang/master/include/version.h",
                     f"{datadir}newestjaclangversion.txt")

    # open version file
    with open(datadir + "newestjaclangversion.txt") as newest_version_file:
        global newest_version
        # parse version file
        newest_version = "BETA " + ".".join([line.split(" ")[2][1:-1] for line in
                                             newest_version_file.read().split("\n") if line])
        try:
            currentjaclangversion = check_output(["jaclang", "--version"]).decode("utf-8")[:-1]
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
    if not checkForJaclangUpgrade():
        print("Jaclang is up to date.")
    else:
        upgradeJaclang()


def checkForJaclangUpdate():
    if checkForJaclangUpgrade():
        print("Jaclang needs to be updated! Update it by typing jpm upgrade!")
