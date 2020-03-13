import bs4
from scripts.listall import list_url_dir
from globals import print_normal, print_debug


def updatedatabase():
    print_normal("Updating database...")
    print_debug("Getting data ... ", end='', flush=True)
    packages = list_url_dir("https://jaclang.zorz.si/main-repository/metadatas/")
    print_debug("DONE")
    print_debug("Writing data ... ", end='', flush=True)
    with open("/usr/local/share/jaclang-data/jpm-database.txt", "w") as database:
        database.write("\n".join(packages))
    print_debug("DONE")
    print_normal(end='')
