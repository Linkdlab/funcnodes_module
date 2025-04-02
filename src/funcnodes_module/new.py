from os import system as ossystem, popen as ospopen
from typing import Union
from pathlib import Path
import shutil
from .config import template_path, gitpaths
from .utils import create_names, replace_names, read_file_content, write_file_content
from ._git import init_git
from ._react import init_react


def create_new_project(
    name: str, path: Union[Path, str], with_react=False, nogit=False
):
    path = Path(path).absolute()
    basepath = path / name
    srcpath = basepath / "src"
    module_name = name.replace(" ", "_").replace("-", "_").lower()
    package_name = module_name.replace("_", "-")

    project_name, module_name, package_name = create_names(name)

    print(f"Creating project {name} at {basepath}")
    ossystem("python -m pip install uv --upgrade")

    if basepath.exists() and basepath.is_dir():
        # check if empty
        if any(basepath.iterdir()):
            print(f"Project {name} already exists")
            return
        else:
            print(f"Project {name} already exists but is empty")
            basepath.rmdir()

    shutil.copytree(template_path, basepath)

    # get current git user

    git_user = ospopen("git config user.name").read().strip() or "Your Name"
    git_email = ospopen("git config user.email").read().strip() or "your.email@send.com"

    # in each file replace "{{ project_name }}" with name
    # and "{{ git_user }}" with git_user
    # and "{{ git_email }}" with git_email

    for file in basepath.rglob("*"):
        if file.is_file():
            try:
                content, enc = read_file_content(file)
            except UnicodeDecodeError:
                print(f"Error reading file {file}")
                continue
            content = replace_names(
                content,
                project_name=project_name,
                module_name=module_name,
                package_name=package_name,
                git_user=git_user,
                git_email=git_email,
            )
            write_file_content(file, content, enc)

    # rename the new_package folder to the project name
    (srcpath / "new_package").rename(srcpath / module_name)

    # rename all files starting with "template__" by removing the "template__" prefix
    for file in basepath.rglob("*"):
        if file.is_file() and file.name.startswith("template__"):
            new_name = file.name.replace("template__", "")
            file.rename(file.with_name(new_name))

    if not nogit:
        init_git(basepath)
    else:
        for gitpath in gitpaths:
            gitpath = basepath / gitpath
            if gitpath.exists() and gitpath.is_dir():
                shutil.rmtree(gitpath)

    reactfolder = srcpath / "react_plugin"
    if not with_react and reactfolder.exists() and reactfolder.is_dir():
        shutil.rmtree(reactfolder)
    else:
        init_react(reactfolder)
        # remove the .git and .gitignore
