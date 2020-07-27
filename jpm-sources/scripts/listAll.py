from urllib import request
from bs4 import BeautifulSoup

from globals import main_repository
from scripts.listPackages import printPackages


def listUrlDir(url):
    page = request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    return [node.get('href').split("/")[0] for node in soup.find_all('a') if node.get('href').endswith("/") and node.get('href') != "/"]


def listall():
    print("Listing all installable packages:")
    printPackages(listUrlDir(main_repository))
