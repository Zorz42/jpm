from globals import *


def fail(print_result):
    if print_result:
        print_debug("FAILED")


def verify_package_json(json, package_name, print_result=True):
    if print_result:
        print_debug("Verifying " + package_name + " ... ", end='', flush=True)
    if not (
            "type" in json.keys() and
            "version" in json.keys()
    ):
        fail(print_result)
        return False
    if type(json["type"]) is not str:
        fail(print_result)
        return False
    if type(json["version"]) is not str:
        fail(print_result)
        return False
    if "dependencies" in json.keys():
        if not all(isinstance(x, str) for x in json["dependencies"]):
            fail(print_result)
            return False
    if print_result:
        print_debug("DONE")
    return True
