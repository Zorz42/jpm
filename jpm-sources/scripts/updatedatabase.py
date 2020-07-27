from globals import main_repository
from scripts.listall import list_url_dir

install_directory = "/usr/local/share/"


def updatedatabase():
    print("Updating database...")
    packages = list_url_dir(main_repository)
    with open(f"{install_directory}jaclang-data/jpm-database.txt", "w") as database:
        database.write("\n".join(packages) + "\n")
