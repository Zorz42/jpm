from globals import print_debug


def fail(print_result):
    if print_result:
        print_debug("FAILED")


def verify_package_json(json, package_name, print_result=True):
    if print_result:
        print_debug("Verifying " + package_name + " ... ", end='', flush=True)
    needed_keys = ["Version", "Supported Version", "Dependencies"]
    for key in needed_keys:
        if key not in json.keys():
            fail(print_result)
            return False

    if type(json["Version"]) is not str:
        fail(print_result)
        return False
    if type(json["Supported Version"]) is not str:
        fail(print_result)
        return False
    print(json["Dependencies"] is list)
    if not (type(json["Dependencies"]) is list and all(type(x) is str for x in json["Dependencies"])):
        fail(print_result)
        return False

    supported_version = json["Supported Version"].split(".")
    print_debug(supported_version)

    if print_result:
        print_debug("DONE")
    return True
