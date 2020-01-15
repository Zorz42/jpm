from json import load
from os import path, remove

from globals import print_error, print_normal, abort, metadatadir, choice, list_packages_print, print_debug
from scripts.verify import verify_package_json


def fail(text):
    print_debug("FAILED")
    print_error(text)
    abort()


def remove_packages(package_names, force=False):
    print_debug("Verifying packages ... ", end='', flush=True)
    for package in package_names:
        if not path.isfile(metadatadir + package + ".json"):
            print_debug("FAILED")
            print_error("Package " + package + " is not installed.")
            abort()
        with open(metadatadir + package + ".json") as file:
            metadata = load(file)
            if not verify_package_json(metadata, package, False):
                fail("Package " + package + " does not have a valid json file.")
            elif metadata['type'] == 'dependency' and not force:
                fail("Package " + package + " is a dependency and is probably needed by other packages. "
                                            "If you want to remove unused dependencies type 'jpm cleanup'.")
    print_debug("DONE")
    print_normal("Following packages will be removed:")
    list_packages_print(package_names)
    if choice():
        print_debug(end='')
        for package in package_names:
            print_debug("Removing " + package + " ... ", end='', flush=True)
            remove(metadatadir + package + ".json")
            print_debug("DONE")
    else:
        abort()
    print_normal("Removed " + str(len(package_names)) + " packages.")
