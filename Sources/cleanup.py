from os import unlink, path
from shutil import rmtree

from globals import choice, libdir, printException
from listPackages import printPackages
from remove import removePackages, PackageError
from checkForUnusedPackages import checkForUnusedPackages


def cleanup():
    # remove unused packages and invalid files
    unused_packages, to_remove, _ = checkForUnusedPackages(set())

    if not unused_packages:
        print("All packages are being used.")
    else:
        try:
            removePackages(unused_packages, force=True)
        except PackageError as e:
            printException(e)

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
