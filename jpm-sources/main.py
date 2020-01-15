import sys

if sys.version_info.major != 3:
    print_error("Must be using Python3")
    exit(1)

from scripts.install import *
from scripts.cleanup import *
from scripts.upgrader import *
from scripts.repair import *

print_debug("JPM installed in " + currentdir)

if len(sys.argv) == 1:
    print_normal("JPM help:")
    print_normal("    jpm install [packages] - install packages")
    print_normal("    jpm remove [packages]  - remove packages")
    print_normal("    jpm list               - list all installed packages")
    print_normal("    jpm cleanup            - clean up unused dependencies and invalid files")
    print_normal("    jpm upgrade [argument] - upgrade to specified version if not specified, upgrade to latest if exists, master is latest, but unstable version")
    print_normal("    jpm repair             - if your jpm is throwing error try this. You might get rid of them.")
    exit(0)

arg = sys.argv[1]
args = sys.argv[2:]

# check or jpm update (upgrade)
def check_for_jpm_update():
    if check_for_upgrade():
        print_normal("JPM needs to be updated! Update it by typing jpm upgrade!")
        print_debug(end="")
    else:
        print_debug("JPM is up to date.")

def check_connection():
    if not check_internet_connection():
        print_error("Cannot connect to the internet (zorz.si)")
        exit(1)

if arg == "install":
    check_connection()
    check_for_jpm_update()
    install(args)
elif arg == "remove":
    remove(args)
    cleanup()
elif arg == "list":
    list_packages()
elif arg == "cleanup":
    cleanup()
elif arg == "upgrade" and len(args) > 0:
    check_connection()
    forceupgrade("v" + args[0])
elif arg == "upgrade":
    check_connection()
    upgrade()
elif arg == "repair":
    repair()
else:
    print_error("Unknown argument: " + arg)
    exit(1)
