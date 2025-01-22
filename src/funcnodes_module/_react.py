import os


def _init_react(basepath):
    os.chdir(basepath)
    # install yarn if not installed
    os.system("npm install -g yarn")
    # install react
    os.system("yarn install")
