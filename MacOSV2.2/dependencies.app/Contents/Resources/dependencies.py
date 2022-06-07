import os

os.system("sudo spctl --master-disable")
os.system("xcode-select --install")
os.system('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"')
os.system("brew install zbar")




