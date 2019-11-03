def verify_package_json(json, package_name, print_result=True):
    if print_result:
        print("Verifying " + package_name + " ... ", end='', flush=True)
    if not (
        "type" in json.keys() and
        "version" in json.keys()
    ):
        if print_result:
            print("FAILED")
        return False
    if type(json["type"]) is not str:
        if print_result:
            print("FAILED")
        return False
    if type(json["version"]) is not str:
        if print_result:
            print("FAILED")
        return False
    if "dependencies" in json.keys():
        if not all(isinstance(x, str) for x in json["dependencies"]):
            if print_result:
                print("FAILED")
            return False
    if print_result:
        print("DONE")
    return True