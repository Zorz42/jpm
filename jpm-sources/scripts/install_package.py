import json

from globals import *


def install_package(package_name, dependency):
    with open(installdir + package_name + ".json") as metafile:
        metadata = json.load(metafile)
    with open(installdir + package_name + ".json", "w") as metafile:
        if dependency:
            metadata['type'] = 'dependency'
        json.dump(metadata, metafile, indent=4)
    os.system("mv " + installdir + package_name + ".json " + metadatadir)
    """files_to_download = []
    if 'files' in metadata.keys():
        files_to_download = [metadata['files']]"""  # code for later
