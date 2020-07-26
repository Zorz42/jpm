from json import load, dump
from os import system

from globals import installdir, libdir


def install_package(package_name, dependency):
    with open(f"{installdir}{package_name}.json", "r+") as info_file:
        metadata = load(info_file)
        metadata["Type"] = "Dependency" if dependency else "Package"
        dump(metadata, info_file, indent=4)
        info_file.write("\n")
    system(f"mv {installdir}{package_name}.json {libdir}")
