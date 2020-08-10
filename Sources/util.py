from json import load, dump
from os import mkdir, remove, path
from tarfile import open as tar_open
from urllib.request import urlopen, Request
from urllib.error import HTTPError


def writeInfo(json: dict, file_path: str):
    with open(file_path, "w") as file:
        file.seek(0)
        dump(json, file, indent=4)
        file.write('\n')
        file.truncate()


def loadInfo(file_path: str):
    with open(file_path) as file:
        return load(file)


def extractTar(tar_path: str, directory_path: str, remove_tar=False):
    mkdir(directory_path)
    with tar_open(tar_path, "r:gz") as tar_file:
        tar_file.extractall(path=directory_path)
    if remove_tar:
        remove(tar_path)


def removeFileIfExists(file_path: str):
    if path.isfile(file_path):
        remove(file_path)


def downloadFile(url: str, file_destination: str):
    with urlopen(url) as f:
        html = f.read()
    with open(file_destination, "wb") as file:
        file.seek(0)
        file.write(html)
        file.truncate()


def urlExists(url: str):
    request = Request(url)
    request.get_method = lambda: 'HEAD'

    try:
        urlopen(request)
        return True
    except HTTPError:
        return False
