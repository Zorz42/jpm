from globals import main_repository
from scripts.listAll import listUrlDir

install_directory = "/usr/local/share/"


def updatedatabase():
    print("Updating database...")
    packages = listUrlDir(main_repository)
    with open(f"{install_directory}jaclang-data/jpm-database.txt", "w") as database:
        database.write("\n".join(packages) + "\n")
