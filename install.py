import sys
from os import popen, system, path
import platform

python3 = sys.version_info.major == 3

def decision(question):
	yesOptions = ["Y", "YES"]
	noOptions  = ["N", "NO"]
	while True:
		try:
			if(python3):
				decision = input(question + " [y,n]:")
			else:
				decision = raw_input(question + " [y,n]:")
		except:
			pass
		
		if decision.upper() in yesOptions:
			return True
		elif decision.upper() in noOptions:
			return False

def check_for_package(name, binary, install_command):
	prefix = name.upper() + " ... "
	if popen("which " + name).read() == "":
		print(prefix + "FAILED")
		if(decision("Do you want me to install " + name + "?")):
			system(install_command)
		else:
			exit(1)
	else:
		print(prefix + "OK")

if len(sys.argv) == 1:
	print("If you have python3 installed:")
	print("	python3 install.py dependencies")
	print("	python3 install.py install")
	print("If you have python2 installed:")
	print("	python install.py dependencies")
	print("	python3 install.py install")
	print("If you do not have python installed, then install python (python3 recommended)")

elif len(sys.argv) == 2:
	if sys.argv[1] == "install":
		if platform.system() == 'Linux':
			system("sudo cp -r jpm-sources/ /usr/local/bin")
		elif platform.system() == 'Darwin':
			system("sudo cp -r jpm-sources/ /usr/local/bin/jpm-sources")
		else:
			print("Unsuported os!")
		system("sudo cp jpm /usr/local/bin")
		system("sudo chmod +x /usr/local/bin/jpm")
		print("JPM installed sucsessfully! Type jpm in terminal for help.")
	
	elif sys.argv[1] == "dependencies":

		if platform.system() == 'Linux':
			current_package_manager = ''
			package_managers = ['apt', 'yum', 'emerge', 'pacman', 'zypper']
			for package_manager in package_managers:
				if popen("which " + package_manager).read() != "":
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
			check_for_package("python3-pip3", "python3-pip3", "sudo " + current_package_manager + " python3-pip")
			check_for_package("pip3-wget", "cannot-check", "pip3 install wget")

		elif platform.system() == 'Darwin':

			print("Checking for dependencies:")
			check_for_package("brew", "brew", '/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
			check_for_package("python3", "python3", "brew install python3")
			check_for_package("python3-pip3", "python3-pip3", "brew install python3-pip")
			check_for_package("pip3-wget", "cannot-check", "pip3 install wget")

		else:
			print("Unsuported os!")
	else:
		print("Invalid argument: " + sys.argv[1])
else:
	print("Only one argument allowed!")
