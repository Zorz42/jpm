from requests import head, exceptions

from globals import throwError


def checkRepConnection():
    try:
        head("https://zorz.si")
        return True
    except exceptions.ConnectionError:
        return False


def checkConnection():
    if not checkRepConnection():
        throwError("Cannot connect to the repository!")
