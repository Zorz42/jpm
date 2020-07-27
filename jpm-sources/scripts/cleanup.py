from json import load
from os import remove

from globals import choice, libdir
from scripts.listPackages import list_installed_packages, print_packages
from scripts.remove import remove_packages

used_packages = []
infos = {}


def list_dependencies(package_name):
    if package_name not in used_packages:
        used_packages.append(package_name)
        for package in infos[package_name]["Dependencies"]:
            list_dependencies(package)


def cleanup():
    installed_packages, to_remove = list_installed_packages()

    for package in installed_packages:
        with open(f"{libdir}{package}/Info.json") as file:
            infos[package] = load(file)

    dependencies = []
    packages = []
    for package in installed_packages:
        if infos[package]['Type'] == 'Package':
            packages.append(package)
        else:
            dependencies.append(package)

    for package in packages:
        list_dependencies(package)
    unused_packages = [x for x in installed_packages if x not in used_packages]

    if not unused_packages:
        print("All packages are being used.")
    else:
        remove_packages(unused_packages, True)

    if to_remove:
        print("Following files/directories do not belong into jaclang-libraries and will be removed:")
        print_packages(to_remove)
        if choice():
            for file in to_remove:
                remove(libdir + file)
            print(f"Removed {len(to_remove)} files/directories.")
        else:
            exit(0)
