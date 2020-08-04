from sys import version_info, argv
from subprocess import call

from globals import throwError

version = "1.6.11"


def getSuperuserPrivileges():
    if call(["/usr/bin/sudo", "/usr/bin/id"]) != 0:
        exit(0)


def main():
    if version_info.major != 3:
        throwError("Must be using Python3")

    if len(argv) == 1:
        print(f"Jpm {version} - help:")
        with open("/usr/local/Jac/Data/jpm-help.txt") as help_file:
            print(help_file.read(), end='')
        return

    arg = argv[1]
    args = argv[2:]

    if arg == "install":
        from scripts.install import install
        from scripts.checkForRepositoryConnection import checkConnection
        from scripts.upgrader import checkForJaclangUpdate

        getSuperuserPrivileges()
        checkForJaclangUpdate()
        checkConnection()
        install(set(args))
    elif arg == "remove":
        from scripts.remove import removePackages
        from scripts.upgrader import checkForJaclangUpdate

        getSuperuserPrivileges()
        checkForJaclangUpdate()
        removePackages(set(args))
    elif arg == "list":
        from scripts.listPackages import listPackages

        listPackages()
    elif arg == "cleanup":
        from scripts.cleanup import cleanup
        from scripts.upgrader import checkForJaclangUpdate

        getSuperuserPrivileges()
        checkForJaclangUpdate()
        cleanup()
    elif arg == "upgrade":
        from scripts.upgrader import upgrade
        from scripts.checkForRepositoryConnection import checkConnection

        getSuperuserPrivileges()
        checkConnection()
        upgrade()
    elif arg == "listall":
        from scripts.listAll import listall
        from scripts.upgrader import checkForJaclangUpdate

        getSuperuserPrivileges()
        checkForJaclangUpdate()
        listall()
    elif arg == "updatedatabase":
        from scripts.updateDatabase import updateDatabase
        from scripts.checkForRepositoryConnection import checkConnection

        getSuperuserPrivileges()
        checkConnection()
        updateDatabase()
    elif arg == "uninstall":
        from scripts.uninstall import uninstall

        getSuperuserPrivileges()
        uninstall()
    else:
        throwError("Unknown argument: " + arg)


if __name__ == "__main__":
    main()
