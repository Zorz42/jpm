from globals import throwError, urlExists


def checkRepConnection():
    return urlExists("https://jaclang.zorz.si")


def checkConnection():
    if not checkRepConnection():
        throwError("Cannot connect to the repository!")
