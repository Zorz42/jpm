import shutil

from scripts.list_packages import *
from scripts.remove import *

used_packages = []
metadatas = {}


def list_dependencies(package_name):
    if package_name not in used_packages:
        used_packages.append(package_name)
        if 'dependencies' not in metadatas.keys():
            for package in metadatas[package_name]['dependencies']:
                list_dependencies(package)


def cleanup():
    print("Starting cleanup")
    print("Getting installed packages ... ", end='', flush=True)
    (installed_packages, to_remove) = list_installed_packages()
    print("DONE")
    print("Getting metadatas of installed packages ... ", end='', flush=True)
    for package in installed_packages:
        with open(metadatadir + package + ".json") as file:
            metadatas[package] = json.load(file)
    print("DONE")
    print("Listing dependencies and packages ... ", end='', flush=True)
    dependencies = []
    packages = []
    for package in installed_packages:
        if metadatas[package]['type'] == 'package':
            packages.append(package)
        else:
            dependencies.append(package)
    print("DONE")
    print("Listing unused packages ... ", end='', flush=True)
    for package in packages:
        list_dependencies(package)
    unused_packages = [x for x in installed_packages if x not in used_packages]
    print("DONE\x1b[0m")
    if not unused_packages:
        print("All packages are being used.")
    else:
        remove(unused_packages, True)
    if to_remove:
        print("Following files/directories are not valid packages and thus do not belong here and will be deleted:")
        list_packages_print(to_remove)
        if choice():
            for file in to_remove:
                if os.path.isfile(metadatadir + file):
                    os.remove(metadatadir + file)
                else:
                    shutil.rmtree(metadatadir + file)
            print("Removed " + str(len(to_remove)) + " files/directories.")
        else:
            print("\x1b[0;31mAborting")
            exit(0)
