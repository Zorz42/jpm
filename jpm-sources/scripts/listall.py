from globals import print_normal, list_packages_print
from bs4 import BeautifulSoup
import requests


def list_url_dir(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return [(url + '/' + node.get('href')).split("/")[-1].split(".")[0] for node in soup.find_all('a')
            if node.get('href').endswith("json")]


def listall():
    print_normal("Listing all installable packages:")
    list_packages_print(list_url_dir("https://jaclang.zorz.si/main-repository/metadatas/"))
