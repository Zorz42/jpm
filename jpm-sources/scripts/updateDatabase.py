from urllib import request
from bs4 import BeautifulSoup

from globals import main_repository


def listUrlDir(url: str):
    return [node.get("href").split("/")[0] for node in BeautifulSoup(request.urlopen(url), "html.parser").find_all("a")
            if node.get("href").endswith("/") and node.get("href") != "/"]


def updateDatabase():
    print("Updating database...")
    packages = listUrlDir(main_repository)
    with open(f"/usr/local/share/jaclang-data/jpm-database.txt", "w") as database:
        database.write("\n".join(packages))
