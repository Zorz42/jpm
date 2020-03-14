from urllib import request

from bs4 import BeautifulSoup

from globals import print_normal, list_packages_print


def list_url_dir(url):
    page = request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    return [(url + '/' + node.get('href')).split("/")[-1].split(".")[0] for node in soup.find_all('a')
            if node.get('href').endswith("json")]


def listall():
    print_normal("Listing all installable packages:")
    list_packages_print(list_url_dir("https://jaclang.zorz.si/main-repository/metadatas/"))
