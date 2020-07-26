def verify_package_json(json):
    needed_keys = ["Version", "Supported Version", "Dependencies"]
    for key in needed_keys:
        if key not in json.keys():
            return False

    if type(json["Version"]) is not str:
        return False
    if type(json["Supported Version"]) is not str:
        return False
    if not (type(json["Dependencies"]) is list and all(type(x) is str for x in json["Dependencies"])):
        return False

    return True
