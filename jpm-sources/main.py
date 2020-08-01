from sys import version_info, argv

from globals import throwError

version = "1.6.2"


def main():
    if version_info.major != 3:
        throwError("Must be using Python3")

    if len(argv) == 1:
        print(f"Jpm {version} - help:")
        print("    jpm install [packages] - install packages")
        print("    jpm remove [packages]  - remove packages")
        print("    jpm list               - list all installed packages")
        print("    jpm cleanup            - clean up unused dependencies and invalid files")
        print("    jpm upgrade            - upgrade jaclang to latest stable version")
        print("    jpm listall            - list all packages in repositories")
        print("    jpm updatedatabase     - update database")
        print("    jpm uninstall          - uninstall jpm and any other software in his family, like jaclang")
        return

    arg = argv[1]
    args = argv[2:]
    from scripts.upgrader import checkForJaclangUpdate
    checkForJaclangUpdate()

    if arg == "install":
        from scripts.install import install
        from scripts.checkForRepositoryConnection import checkConnection

        checkConnection()
        install(set(args))
    elif arg == "remove":
        from scripts.remove import removePackages

        removePackages(set(args))
    elif arg == "list":
        from scripts.listPackages import listPackages

        listPackages()
    elif arg == "cleanup":
        from scripts.cleanup import cleanup

        cleanup()
    elif arg == "upgrade":
        from scripts.upgrader import upgrade
        from scripts.checkForRepositoryConnection import checkConnection

        checkConnection()
        upgrade()
    elif arg == "listall":
        from scripts.listAll import listall

        listall()
    elif arg == "updatedatabase":
        from scripts.updateDatabase import updateDatabase
        from scripts.checkForRepositoryConnection import checkConnection

        checkConnection()
        updateDatabase()
    elif arg == "uninstall":
        from scripts.uninstall import uninstall

        uninstall()
    else:
        throwError("Unknown argument: " + arg)


if __name__ == "__main__":
    main()
