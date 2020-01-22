import platform
import sys
from os import popen, system, path, mkdir, environ
from getpass import getuser

python3 = sys.version_info.major == 3

bin_paths = environ["PATH"].split(":")


def decision(question):
    yesOptions = ["Y", "YES"]
    noOptions = ["N", "NO"]
    while True:
        if python3:
            decisionBool = input(question + " [y,n]:")
        else:
            decisionBool = raw_input(question + " [y,n]:")

        if decisionBool.upper() in yesOptions:
            return True
        elif decisionBool.upper() in noOptions:
            return False


def check_for_package(name, binary, install_command):
    print(name.upper() + ' ... ', end='')
    for bin_path in bin_paths:
        if path.isfile(bin_path + "/" + binary):
            print("OK")
            break
    else:
        print("FAILED")
        if decision("Do you want me to install " + name + "?"):
            system(install_command)
        else:
            exit(1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("If you have python3 installed:")
        print("	python3 install.py dependencies")
        print("	python3 install.py install")
        print("If you have python2 installed:")
        print("	python install.py dependencies")
        print("	python3 install.py install")
        print("If you do not have python installed, then install python2 or python3 (python3 recommended)")

    elif len(sys.argv) == 2:
        dirs = ['to_install', 'librarysources', 'metadatas']
        for Dir in dirs:
            if not path.isdir("jpm-sources/" + Dir):
                mkdir('jpm-sources/' + Dir)
        if sys.argv[1] == "install" or sys.argv[1] == "quietinstall":
            print("test")
            if platform.system() == 'Linux':
                system("sudo cp -r jpm-sources/ /usr/local/bin")
            elif platform.system() == 'Darwin':
                system("sudo cp -r jpm-sources/ /usr/local/bin/jpm-sources")
            else:
                print("Unsupported os!")
            system("sudo cp jpm /usr/local/bin")
            if sys.argv[1] == "install":
                print("JPM installed successfully! Type jpm in terminal for help.")

        elif sys.argv[1] == "dependencies":

            if platform.system() == 'Linux':
                current_package_manager = ''
                package_managers = ['apt', 'yum', 'emerge', 'pacman', 'zypper']
                for package_manager in package_managers:
                    if popen("which " + package_manager).read():
                        if package_manager == 'apt':
                            current_package_manager = 'apt install'
                        elif package_manager == 'yum':
                            current_package_manager = 'yum install'
                        elif package_manager == 'emerge':
                            current_package_manager = 'emerge'
                        elif package_manager == 'pacman':
                            current_package_manager = 'pacman -S'
                        elif package_manager == 'zypper':
                            current_package_manager = 'zypper in'
                        break
                if current_package_manager == '':
                    print('Could not find package manager!')
                    exit(1)

                print("Checking for dependencies:")
                check_for_package("python3", "python3", "sudo " + current_package_manager + " python3")
                check_for_package("python3-pip", "pip3", "sudo " + current_package_manager + " python3-pip")

            elif platform.system() == 'Darwin':

                print("Checking for dependencies:")
                check_for_package("brew", "brew",
                                  '/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install'
                                  '/master/install)"')
                check_for_package("python3", "python3", "brew install python3")
            else:
                print("Unsuported os!")
            if python3:
                from checkforpippackages import *
                checkforpippackages_main()
            else:
                system("python3 checkforpippackages.py")
        else:
            print("Invalid argument: " + sys.argv[1])
    else:
        print("Only one argument allowed!")
