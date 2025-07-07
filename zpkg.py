# imports
import sys
import subprocess
import os
import pyfiglet
from colorama import Fore, Style, init
import platform
import time
from pathlib import Path
init() # colorama init
BANNER = pyfiglet.figlet_format("ZPKG") # figlet ascii art
CLEAR = "clear" # clear command
POS = f"{Style.BRIGHT}{Fore.MAGENTA}[{Fore.GREEN}+{Fore.RESET}{Fore.MAGENTA}]{Style.RESET_ALL}" # positive info
NEG = f"{Style.BRIGHT}{Fore.MAGENTA}[{Fore.RED}-{Fore.RESET}{Fore.MAGENTA}]{Style.RESET_ALL}" # negative info
URG = f"{Style.BRIGHT}{Fore.MAGENTA}[{Fore.YELLOW}*{Fore.RESET}{Fore.MAGENTA}]{Style.RESET_ALL}" # urgent info
OPTIONS = "\n1. Install Packages\n2. Create Install List\n3. Exit\n\n" # user options

if platform.system().lower() != 'linux': # if detected system is not linux
    print(f"{NEG} Z2PKG only works for linux.")
    finalise()
    sys.exit(0) # exit

def get_install_command(): # function to detect package manager install command
    try:
        install = ['apt', 'install', '-y'] # default to apt
        try:
            with open("/etc/os-release") as f: # read os-release to determine linux distribution
                lines = f.readlines()

            os_info = {}
            for line in lines:
                if '=' in line:
                    key, val = line.strip().split('=', 1)
                    os_info[key] = val.strip('"')

            distro = os_info.get("ID", "").lower()
            if distro == "fedora":
                print(f"{POS} Using {Fore.CYAN}{Style.BRIGHT}DNF{Style.RESET_ALL} package manager")
                install = ['dnf', 'install', '-y']
            elif distro in ["debian", "ubuntu", "pop"]:
                print(f"{POS} Using {Fore.CYAN}{Style.BRIGHT}APT{Style.RESET_ALL} package manager")
                install = ['apt', 'install', '-y']
            elif distro in ["arch", "manjaro"]:
                print(f"{POS} Using {Fore.CYAN}{Style.BRIGHT}PACMAN{Style.RESET_ALL} package manager")
                install = ['pacman', '-S', '--noconfirm']
            elif distro in ["opensuse", "sles"]:
                print(f"{POS} Using {Fore.CYAN}{Style.BRIGHT}ZYPPER{Style.RESET_ALL} package manager")
                install = ['zypper', 'install', '-y']
        except Exception:
            print(f"{NEG} Could not detect linux distribution.\n{POS} Defaulting to APT")

        if os.geteuid() != 0: # script assumes user is root, if not add sudo to the start of each install command
            install.insert(0, 'sudo') 

        return install
    except KeyboardInterrupt: # detect sigterm
        print(f"{NEG} Aborted by user.")
        time.sleep(1)
        finalise()

def finalise(): # function to end script
    subprocess.run([CLEAR], shell=True) # clear screen
    print(Fore.BLUE + Style.BRIGHT + BANNER + Style.RESET_ALL) # print banner
    print(f"{POS} Thank you for using ZPKG.\n\n\n") 
    sys.exit(0)

def installpkg(): # function to install packages
    try:
        INSTALL = get_install_command() # determine package mananger install command
        PACKAGES = [] # create empty list of packages
        current_dir = Path('.') # detect current directory
        for file in current_dir.glob('*.zpkg'): # find files in current directory with file extension .zpkg
            print(f"{POS} Found -> {file.resolve()}") 
        print(f"{URG} Please enter the path of the {Fore.CYAN}{Style.BRIGHT}.zpkg{Style.RESET_ALL} list.")
        try:
            PKGLIST = Path(input(Fore.BLUE + Style.BRIGHT + "Z> " + Style.RESET_ALL)) # input zpkg file path
            if PKGLIST == "." or ".." or "...":
                raise IsADirectoryError
        except IsADirectoryError:
            print(f"{NEG} Path is a directory, not a zpkg file.")
            time.sleep(2)
            return
        if PKGLIST.exists():
            print(f"{POS} Found {Fore.CYAN}{PKGLIST}{Style.RESET_ALL}") # successfully found file
        else:
            print(f"{NEG} Could not find {Fore.RED}{PKGLIST}{Style.RESET_ALL}") # could not find file
            time.sleep(2) # needs to sleep or else user wont see the error
            return
        with open(PKGLIST, "r") as pkglist: # read the file
            for package in pkglist: # for every line 
                PACKAGES.append(package.strip()) # strip and append the line to the packages list
        print(f"{POS} Current Packges: {PACKAGES}") # print packages to install
        print(f"{URG} Install? [y/N]") # prompt to install, defaults to no 
        startinstall = input(Fore.BLUE + Style.BRIGHT + "Z> " + Style.RESET_ALL).lower().strip() 
        if startinstall not in ['yes', 'y']: # if user doesnt enter yes or y
            print(f"{NEG} Installation aborted by user.")
            time.sleep(4)
            return
        print(f"{POS} Starting installation...") # begin the install
        try:
            for PACKAGE in PACKAGES: 
                print(f"{POS} Installing {PACKAGE}...")
                subprocess.run(INSTALL + [PACKAGE]) # install the package
            subprocess.run([CLEAR], shell=True)
            print(Fore.BLUE + Style.BRIGHT + BANNER + Style.RESET_ALL)
            print(f"{POS} Complete!") # success
        except Exception as e:
            print(f"{NEG} Error: {e}")
            time.sleep(3)
        time.sleep(4)
    except KeyboardInterrupt:
        print(f"{NEG} Aborted by user.")
        time.sleep(1)
        finalise()


def createpkgs(): # create zpkg file
    try:
        print(f"{URG} Enter filename without extension")
        FILENAME = input(Fore.BLUE + Style.BRIGHT + "Z> " + Style.RESET_ALL) # append zpkg as file extension
        if not FILENAME:
            print(f"{NEG} Invalid filename")
            time.sleep(2)
            return
        FILENAME = FILENAME + '.zpkg'
        print(f"{URG} Enter packages (comma seperated)") # enter packages
        PACKAGES = input(Fore.BLUE + Style.BRIGHT + "Z> " + Style.RESET_ALL)
        PKGLIST = [pkg.strip() for pkg in PACKAGES.split(',') if pkg.strip()] # split each package with comma
        with open(FILENAME, "w") as f: # write to zpkg file
            for pkg in PKGLIST:
                f.write(pkg + "\n")
        print(f"{POS} Saved to {FILENAME}")
        time.sleep(4)
    except KeyboardInterrupt:
        print(f"{NEG} Aborted by user.")
        time.sleep(1)
        finalise()

def menu():
    try:
        choice = 0 # initialise choice with value 0
        while choice != 3: # while loop infinitely unless user selects to exit
            subprocess.run([CLEAR], shell=True) # clear screen
            print(Fore.BLUE + Style.BRIGHT + BANNER + Style.RESET_ALL) # print banner
            print(Fore.CYAN + Style.BRIGHT + OPTIONS + Style.RESET_ALL) # print screen
            try:
                choice = int(input(Fore.BLUE + Style.BRIGHT + "Z> " + Style.RESET_ALL)) # user chooses option
                if choice == 1:
                    installpkg()
                elif choice == 2:
                    createpkgs()
                elif choice == 3:
                    finalise()
                else:
                    print(f"{NEG} Invalid number. Enter from range 1-3.") # error handling stuff
                    time.sleep(2)
            except ValueError:
                print(f"{NEG} Invalid number. Enter from range 1-3.")
                time.sleep(2)
    except KeyboardInterrupt:
        print(f"{NEG} Aborted by user.")
        time.sleep(1)
        finalise()

def main(): # main function
    try:
        menu() #run menu
    except KeyboardInterrupt:
        print(f"{NEG} Aborted by user.")
        time.sleep(1)
        finalise()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{NEG} Aborted by user.")
        time.sleep(1)
        finalise()
