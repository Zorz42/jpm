from os import remove

from globals import choice, libdir
from scripts.listPackages import printPackages
from scripts.remove import removePackages
from scripts.checkForUnusedPackages import checkForUnusedPackages


def cleanup():
    unused_packages, to_remove, _ = checkForUnusedPackages([])

    if not unused_packages:
        print("All packages are being used.")
    else:
        removePackages(unused_packages, force=True)

    if to_remove:
        print("Following files/directories do not belong into jaclang-libraries and will be removed:")
        printPackages(to_remove)
        if choice():
            for file in to_remove:
                remove(libdir + file)
            print(f"Removed {len(to_remove)} files/directories.")
