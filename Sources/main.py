from sys import version_info, argv, path
from globals import printException

path.append("/usr/local/Jac/Jpm")
version = "1.7.10"


class VersionMismatch(Exception):
    pass


class ArgumentError(Exception):
    pass


def main():
    if version_info.major != 3:
        raise VersionMismatch("Must be using Python3")

    if len(argv) == 1:
        print(f"Jpm {version} - help:")
        with open("/usr/local/Jac/Data/jpm-help.txt") as help_file:
            print(help_file.read(), end='')
        return

    arg = argv[1]
    args = argv[2:]

    if arg == "install":
        from install import install
        from checkForRepositoryConnection import checkConnection, InternetConnectionError
        from upgrader import checkForJaclangUpdate

        checkForJaclangUpdate()
        try:
            checkConnection()
        except InternetConnectionError as e_:
            printException(e_)
        install(set(args))
    elif arg == "remove":
        from remove import removePackages, PackageError
        from upgrader import checkForJaclangUpdate

        checkForJaclangUpdate()
        try:
            removePackages(set(args))
        except PackageError as e_:
            printException(e_)
    elif arg == "list":
        from listPackages import listPackages

        listPackages()
    elif arg == "cleanup":
        from cleanup import cleanup
        from upgrader import checkForJaclangUpdate

        checkForJaclangUpdate()
        cleanup()
    elif arg == "upgrade":
        from upgrader import upgrade
        from checkForRepositoryConnection import checkConnection, InternetConnectionError

        try:
            checkConnection()
        except InternetConnectionError as e_:
            printException(e_)
        upgrade()
    elif arg == "listall":
        from listAll import listall
        from upgrader import checkForJaclangUpdate

        checkForJaclangUpdate()
        listall()
    elif arg == "uninstall":
        from uninstall import uninstall

        uninstall()
    else:
        raise ArgumentError(f"Unknown argument: {arg}")


if __name__ == "__main__":
    try:
        main()
    except VersionMismatch as e:
        printException(e)
    except ArgumentError as e:
        printException(e)
