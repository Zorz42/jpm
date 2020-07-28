from urllib import request
from bs4 import BeautifulSoup

from globals import main_repository
from scripts.listPackages import printPackages


def listUrlDir(url: str):
    return [node.get("href").split("/")[0] for node in BeautifulSoup(request.urlopen(url), "html.parser").find_all("a")
            if node.get("href").endswith("/") and node.get("href") != "/"]


def listall():
    print("Listing all installable packages:")
    printPackages(listUrlDir(main_repository))
