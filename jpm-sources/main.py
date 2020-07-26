from sys import version_info, argv

from globals import print_error, jpm_exit

version = "1.5.4"


def main():
    if version_info.major != 3:
        print_error("Must be using Python3")
        jpm_exit(1)

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
        jpm_exit(0)

    arg = argv[1]
    args = argv[2:]

    if arg == "install":
        from scripts.upgrader import check_for_jpm_update
        from scripts.install import install
        from scripts.checkforinternetconnection import check_connection

        check_connection()
        check_for_jpm_update()
        install(args)
    elif arg == "remove":
        from scripts.cleanup import cleanup, remove_packages

        remove_packages(args)
        cleanup()
    elif arg == "list":
        from scripts.list_packages import list_packages

        list_packages()
    elif arg == "cleanup":
        from scripts.cleanup import cleanup

        cleanup()
    elif arg == "upgrade" and len(args) > 0:
        from scripts.upgrader import upgrade_jaclang
        from scripts.checkforinternetconnection import check_connection

        check_connection()
        upgrade_jaclang()
    elif arg == "upgrade":
        from scripts.upgrader import upgrade
        from scripts.checkforinternetconnection import check_connection

        check_connection()
        upgrade()
    elif arg == "listall":
        from scripts.listall import listall
        from scripts.upgrader import check_for_jpm_update
        from scripts.checkforinternetconnection import check_connection

        check_connection()
        check_for_jpm_update()
        listall()
    elif arg == "version":
        print("Current version: " + version)
    elif arg == "updatedatabase":
        from scripts.updatedatabase import updatedatabase
        from scripts.checkforinternetconnection import check_connection

        check_connection()
        updatedatabase()
    elif arg == "uninstall":
        from scripts.uninstall import uninstall

        uninstall()
    else:
        print_error("Unknown argument: " + arg)
        jpm_exit(1)


if __name__ == "__main__":
    main()
