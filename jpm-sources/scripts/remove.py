from globals import *
from scripts.verify import *
import os, json

def remove(package_names, force=False):
    print("Verifying packages ... ", end='', flush='')
    for package in package_names:
        if not os.path.isfile(metadatadir + package + ".json"):
            print("FAILED")
            print("\x1b[0;31mPackage " + package + " is not installed.")
            print("\x1b[0;31mAborting")
            exit(0)
        with open(metadatadir + package + ".json") as file:
            metadata = json.load(file)
            if not verify_package_json(metadata, package, False):
                print("FAILED")
                print("\x1b[0;31mPackage " + package + " does not have a valid json file.")
                print("\x1b[0;31mAborting")
                exit(0)
            elif metadata['type'] == 'dependency' and not force:
                print("FAILED")
                print("\x1b[0;31mPackage " + package + " is a dependency and is probably needed by other packages. If you want to remove packages type 'jpm cleanup'.")
                print("\x1b[0;31mAborting")
                exit(0)
    print("DONE")
    print("\x1b[0mFollowing packages will be removed:")
    list_packages_print(package_names)
    if choice():
        print("\x1b[1;30m", end='')
        for package in package_names:
            print("Removing " + package + " ... ", end='', flush=True)
            os.remove(metadatadir + package + ".json")
            print("DONE")
    else:
        print("\x1b[0;31mAborting")
        exit(0)
    print("\x1b[0mRemoved " + str(len(package_names)) + " packages.")