from util import urlExists


# because ConnectionError is already in builtins
class InternetConnectionError(Exception):
    pass


def checkRepConnection():
    return urlExists("https://jaclang.zorz.si")


def checkConnection():
    if not checkRepConnection():
        raise InternetConnectionError("Cannot connect to the repository!")
