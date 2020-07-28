from urllib.request import urlopen, Request

from globals import main_repository


def listUrlDir(url: str):
    # parse url files
    with urlopen(url) as f:
        html = f.read().decode("utf-8")
    package_names = []
    for line in html.split("\n"):
        if line.startswith("<tr>") and "alt=\"[DIR]\"" in line:
            package_names.append(line[line.find("href") + 6:].partition("\"")[0][:-1])
    return package_names


def updateDatabase():
    print("Updating database...")
    packages = listUrlDir(main_repository)
    with open(f"/usr/local/share/jaclang-data/jpm-database.txt", "w") as database:
        database.write("\n".join(packages))
