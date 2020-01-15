from json import load, dump
from os import system

from globals import installdir, metadatadir


def install_package(package_name, dependency):
    with open(installdir + package_name + ".json") as metafile:
        metadata = load(metafile)
    with open(installdir + package_name + ".json", "w") as metafile:
        if dependency:
            metadata['type'] = 'dependency'
        dump(metadata, metafile, indent=4)
    system("mv " + installdir + package_name + ".json " + metadatadir)
    """files_to_download = []
    if 'files' in metadata.keys():
        files_to_download = [metadata['files']]"""  # code for later
