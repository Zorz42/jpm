from sys import version_info, argv

from globals import throw_error

version = "1.5.4"


def main():
    if version_info.major != 3:
        throw_error("Must be using Python3")

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
        from scripts.upgrader import check_for_jpm_update
        from scripts.install import install
        from scripts.checkForRepositoryConnection import checkConnection

        checkConnection()
        check_for_jpm_update()
        install(args)
    elif arg == "remove":
        from scripts.cleanup import cleanup, remove_packages

        remove_packages(args)
        cleanup()
    elif arg == "list":
        from scripts.listPackages import list_packages

        list_packages()
    elif arg == "cleanup":
        from scripts.cleanup import cleanup

        cleanup()
    elif arg == "upgrade" and len(args) > 0:
        from scripts.upgrader import upgrade_jaclang
        from scripts.checkForRepositoryConnection import checkConnection

        checkConnection()
        upgrade_jaclang()
    elif arg == "upgrade":
        from scripts.upgrader import upgrade
        from scripts.checkForRepositoryConnection import checkConnection

        checkConnection()
        upgrade()
    elif arg == "listall":
        from scripts.listall import listall
        from scripts.upgrader import check_for_jpm_update
        from scripts.checkForRepositoryConnection import checkConnection

        checkConnection()
        check_for_jpm_update()
        listall()
    elif arg == "version":
        print("Current version: " + version)
    elif arg == "updatedatabase":
        from scripts.updatedatabase import updatedatabase
        from scripts.checkForRepositoryConnection import checkConnection

        checkConnection()
        updatedatabase()
    elif arg == "uninstall":
        from scripts.uninstall import uninstall

        uninstall()
    else:
        throw_error("Unknown argument: " + arg)


if __name__ == "__main__":
    main()
