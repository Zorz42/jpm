from urllib import error, request

from globals import throw_error


def checkRepConnection():
    """try:
        ssl._create_default_https_context = ssl._create_unverified_context
    except AttributeError:
        pass"""
    try:
        request.urlopen("https://zorz.si")
        return True
    except error.HTTPError:
        return False


def checkConnection():
    if not checkRepConnection():
        throw_error("Cannot connect to the repository (zorz.si)")
