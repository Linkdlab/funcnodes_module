from pathlib import Path
from os import system as ossystem, getcwd as osgetcwd, chdir as oschdir


def init_react(basepath: Path):
    cd = osgetcwd()
    oschdir(basepath / "")
    # install yarn if not installed
    ossystem("npm install -g yarn")
    # install react
    ossystem("yarn install")
    oschdir(cd)
