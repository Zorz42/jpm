import sys

if sys.version_info.major != 3:
    print("\x1b[0;31mMust be using Python3")
    exit(1)

from scripts.install import *
from scripts.cleanup import *
from scripts.upgrader import *

print("\x1b[1;30m", end='')

if len(sys.argv) == 1:
    print("\x1b[0mJPM help:")
    print("    jpm install [packages] - install packages")
    print("    jpm remove [packages]  - remove packages")
    print("    jpm list               - list all installed packages")
    print("    jpm cleanup            - clean up unused dependencies and invalid files")
    print("    jpm upgrade            - upgrade to newer jpm version (if exists)")
    print("    jpm forceupgrade       - upgrade jpm not matter what (install newest version of jpm even if current jpm is already newest)")
    exit(0)

arg  = sys.argv[1]
args = sys.argv[2:]

# check or jpm update (upgrade)
args_not_to_check_updates = ["list", "upgrade"]
if arg not in args_not_to_check_updates:
    if check_for_upgrade():
        print("\x1b[0mJPM needs to be updated! Update it by typing jpm upgrade!\x1b[1;30m")
    else:
        print("JPM is up to date.")

if arg == "install":
    if not check_internet_connection():
        print("\x1b[0;31mCannot connect to jaclang.zorz.si")
        exit(1)
    install(args)
elif arg == "remove":
    remove(args)
elif arg == "list":
    list_packages()
elif arg == "cleanup":
    cleanup()
elif arg == "upgrade":
    if not check_internet_connection():
        print("\x1b[0;31mCannot connect to jaclang.zorz.si")
        exit(1)
    upgrade()
elif arg == "forceupgrade":
    if not check_internet_connection():
        print("\x1b[0;31mCannot connect to jaclang.zorz.si")
        exit(1)
    forceupgrade()
else:
    print("\x1b[0;31mUnknown argument: " + arg)
    exit(1)

