# zpkg
An automation tool to install packages on linux systems. My first CLI tool.

# Installation guide
Make sure python3 is installed on your system. To install python3 you would run:

APT based system:
``` sudo apt install -y python3 ``` 

DNF based system:
``` sudo dnf install -y python3 ```

PACMAN based system:
``` sudo pacman -S --noconfirm python3 ```

After installing python3, clone the git repo with

``` git clone https://github.com/zzhjf8/zpkg/ ```

``` cd zpkg/ ```

It is recommended to create a virtual environment when install dependencies with pip:

``` python3 -m venv venv ```

``` source ./venv/bin/activate ```

``` pip install -r requirements.txt ```

Next you can launch the script with

``` python3 z2pkg.py ```

Before installing packages, you must make sure you have a .zpkg file which you can also create in the python tool by selecting the option "Create Install List"

You will have to input your desired packages formatted with comma seperaton. For example: ``` htop,alacritty,screenfetch,nasm,vim ```

Run the Install Packages option and input the path of your file. It should detect the package manager and install the packages from the file.

An example install install file is inside this github repo which you can see how the install file is formatted.

## [WARNING] There may be errors in this script as it is my first tool. 





