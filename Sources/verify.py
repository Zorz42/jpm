from os import path
from json import load, decoder

from globals import libdir


def verifyPackageJson(json: dict, installed=True):
    # verify that json has all keys and their valid values
    needed_keys = ["Version", "Dependencies"]
    if not installed:
        needed_keys.append("Supported Version")
    for key in needed_keys:
        if key not in json.keys():
            return False

    if type(json["Version"]) is not str:
        return False
    if not installed and type(json["Supported Version"]) is not str:
        return False
    if not (type(json["Dependencies"]) is list and all(type(x) is str for x in json["Dependencies"])):
        return False

    return True


def packageExists(package_name: str):
    # validate package
    try:
        return path.isfile(f"{libdir}{package_name}/Info.json") \
               and verifyPackageJson(load(open(f"{libdir}{package_name}/Info.json")), installed=True) \
               and path.isfile(f"{libdir}{package_name}/Headers/__main__.jlh")
    except decoder.JSONDecodeError:
        # if json isn't valid
        return False
