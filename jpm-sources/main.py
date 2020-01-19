from sys import version_info, argv

from version import version
from globals import print_normal, print_debug, print_error, jpm_exit, currentdir


def main():
    if version_info.major != 3:
        print_error("Must be using Python3")
        jpm_exit(1)

    print_debug("JPM installed in " + currentdir)

    if len(argv) == 1:
        print_normal("JPM help:")
        print_normal("    jpm install [packages] - install packages")
        print_normal("    jpm remove [packages]  - remove packages")
        print_normal("    jpm list               - list all installed packages")
        print_normal("    jpm cleanup            - clean up unused dependencies and invalid files")
        print_normal(
            "    jpm upgrade [argument] - upgrade to specified version if not specified, upgrade to latest if exists, "
            "master is latest, but unstable version")
        print_normal("    jpm repair             - if your jpm is throwing error try this. You might get rid of them.")
        print_normal("    jpm listall            - list all packages in repositories")
        print_normal("    jpm version            - show current version of jpm")
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
        from scripts.upgrader import forceupgrade
        from scripts.checkforinternetconnection import check_connection

        check_connection()
        forceupgrade("v" + args[0])
    elif arg == "upgrade":
        from scripts.upgrader import upgrade
        from scripts.checkforinternetconnection import check_connection

        check_connection()
        upgrade()
    elif arg == "repair":
        from scripts.repair import repair

        repair()
    elif arg == "listall":
        from scripts.listall import listall
        from scripts.upgrader import check_for_jpm_update
        from scripts.checkforinternetconnection import check_connection

        check_connection()
        check_for_jpm_update()
        listall()
    elif arg == "version":
        print_normal("Current version: " + version)
    else:
        print_error("Unknown argument: " + arg)
        jpm_exit(1)


main()
