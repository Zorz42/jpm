from sys import version_info, argv

from globals import throwError

version = "1.5.4"


def main():
    if version_info.major != 3:
        throwError("Must be using Python3")

    if len(argv) == 1:
        print("JPM help:")
        print("    jpm install [packages] - install packages")
        print("    jpm remove [packages]  - remove packages")
        print("    jpm list               - list all installed packages")
        print("    jpm cleanup            - clean up unused dependencies and invalid files")
        print("    jpm upgrade            - upgrade jaclang to latest stable version")
        print("    jpm listall            - list all packages in repositories")
        print("    jpm version            - show current version of jpm")
        print("    jpm updatedatabase     - update database")
        print("    jpm uninstall          - uninstall jpm and any other software in his family, like jaclang")
        exit(0)

    arg = argv[1]
    args = argv[2:]

    if arg == "install":
        from scripts.upgrader import checkForJaclangUpdate
        from scripts.install import install
        from scripts.checkForRepositoryConnection import checkConnection

        checkConnection()
        checkForJaclangUpdate()
        install(args)
    elif arg == "remove":
        from scripts.remove import removePackages

        removePackages(args)
    elif arg == "list":
        from scripts.listPackages import listPackages

        listPackages()
    elif arg == "cleanup":
        from scripts.cleanup import cleanup

        cleanup()
    elif arg == "upgrade" and len(args) > 0:
        from scripts.upgrader import upgradeJaclang
        from scripts.checkForRepositoryConnection import checkConnection

        checkConnection()
        upgradeJaclang()
    elif arg == "upgrade":
        from scripts.upgrader import upgrade
        from scripts.checkForRepositoryConnection import checkConnection

        checkConnection()
        upgrade()
    elif arg == "listall":
        from scripts.listall import listall
        from scripts.upgrader import checkForJaclangUpdate
        from scripts.checkForRepositoryConnection import checkConnection

        checkConnection()
        checkForJaclangUpdate()
        listall()
    elif arg == "version":
        print("Current version: " + version)
    elif arg == "updatedatabase":
        from scripts.updateDatabase import updatedatabase
        from scripts.checkForRepositoryConnection import checkConnection

        checkConnection()
        updatedatabase()
    elif arg == "uninstall":
        from scripts.uninstall import uninstall

        uninstall()
    else:
        throwError("Unknown argument: " + arg)


if __name__ == "__main__":
    main()
