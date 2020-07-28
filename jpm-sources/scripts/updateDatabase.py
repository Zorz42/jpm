from globals import main_repository
from scripts.listAll import listUrlDir


def updatedatabase():
    print("Updating database...")
    packages = listUrlDir(main_repository)
    with open(f"/usr/local/share/jaclang-data/jpm-database.txt", "w") as database:
        database.write("\n".join(packages) + "\n")
