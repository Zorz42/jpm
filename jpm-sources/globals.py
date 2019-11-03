import os, sys

currentdir = os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0] + '/'
libdir = currentdir + "libsources/"
metadatadir = currentdir + "metadatas/"
installdir = currentdir + "to_install/"

def empty_bar(current, total, width):
    pass

def choice():
    yesOptions = ["Y", "YES"]
    noOptions  = ["N", "NO" ]
    while True:
        print("Proceed?[y,n]:", end='', flush=True)
        answer = input()
        if answer.upper() in yesOptions:
            return True
        elif answer.upper() in noOptions:
            return False

def list_packages_print(package_list):
    for package in package_list:
        print(package, end='     ')
    print()