import sys

if sys.version_info.major != 3:
    print("\x1b[0;31mMust be using Python3")
    exit(1)

from globals import *

from scripts.install import *
from scripts.remove import *
from scripts.list_packages import *
from scripts.cleanup import *

print("\x1b[1;30m", end='')

if len(sys.argv) == 1:
    print("\x1b[0mJPM help:")
    print("    jpm install [packages] - install packages")
    print("    jpm remove [packages]  - remove packages")
    print("    jpm list               - list all installed packages")
    print("    jpm cleanup            - clean up unused dependencies and invalid files")
    exit(0)

arg  = sys.argv[1]
args = sys.argv[2:]

if arg == "install":
    install(args)
elif arg == "remove":
    remove(args)
elif arg == "list":
    list_packages()
elif arg == "cleanup":
    cleanup()
else:
    print("\x1b[0;31mUnknown argument: " + arg)
    exit(1)

