from os import unlink, path
from shutil import rmtree

from globals import choice, libdir
from scripts.listPackages import printPackages
from scripts.remove import removePackages
from scripts.checkForUnusedPackages import checkForUnusedPackages


def cleanup():
    # remove unused packages and invalid files
    unused_packages, to_remove, _ = checkForUnusedPackages(set())

    if not unused_packages:
        print("All packages are being used.")
    else:
        removePackages(unused_packages, force=True)

    if to_remove:
        print("Following files/directories do not belong into jaclang-libraries and will be removed:")
        printPackages(to_remove)
        if choice():
            for file in to_remove:
                if path.isdir(libdir + file):
                    rmtree(libdir + file)
                else:
                    unlink(libdir + file)
            print(f"Removed {len(to_remove)} files/directories.")
