from json import load, dump
from os import remove, path, mkdir
from wget import download
from tarfile import open as tar_open

from globals import installdir, libdir, main_repository, removeFileIfExists


def installPackage(package_name, dependency):
    print(f"Installing {package_name}")
    with open(f"{installdir}{package_name}.json", "r") as info_file:
        info = load(info_file)

    removeFileIfExists(f"{libdir}{package_name}.tar.gz")

    download(f"{main_repository}{package_name}/Versions/{info['Version']}.tar.gz",
             f"{libdir}{package_name}.tar.gz", bar=None)

    mkdir(f"{libdir}{package_name}")
    with tar_open(f"{libdir}{package_name}.tar.gz", "r:gz") as tar_file:
        tar_file.extractall(path=f"{libdir}{package_name}")
    remove(f"{libdir}{package_name}.tar.gz")

    with open(f"{libdir}{package_name}/Info.json", "r+") as info_file:
        metadata = load(info_file)
        metadata["Type"] = "Dependency" if dependency else "Package"
        del metadata["Supported Version"]
        info_file.seek(0)
        dump(metadata, info_file, indent=4)
        info_file.write("\n")
        info_file.truncate()
