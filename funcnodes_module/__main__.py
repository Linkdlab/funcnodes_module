import argparse
import os
import shutil
from . import register

template_path = os.path.join(os.path.dirname(__file__), "template_folder")
files_to_overwrite = [
    os.path.join(".github", "workflows", "py_test.yml"),
    os.path.join(".github", "workflows", "version_publish_main.yml"),
    os.path.join(".github", "workflows", "register_plugin.yml"),
    os.path.join(".github", "actions", "cache_py", "action.yml"),
    os.path.join(".github", "actions", "updates_version", "action.yml"),
    os.path.join(".github", "actions", "install_package", "action.yml"),
    os.path.join("tests", "all_nodes_test_base.py"),
]

files_to_copy_if_missing = [
    os.path.join("tests", "test_all_nodes.py"),
    os.path.join(".pre-commit-config.yaml"),
]


def _init_git(
    path,
):
    current_dir = os.getcwd()
    os.chdir(path)
    # initialize git
    os.system("git init")
    os.system('git commit --allow-empty -m "initial commit"')
    # create a dev and test branch
    os.system("git checkout -b test")
    os.system('git commit --allow-empty -m "initial commit"')
    os.system("git checkout -b dev")

    # # add all files

    os.system("poetry install")
    os.system("poetry add pre-commit@* --group=dev")
    os.system("poetry add pytest@* --group=dev")
    os.system("poetry run pre-commit install")
    os.system("poetry run pre-commit autoupdate")

    os.system("git add .")
    os.system('git commit -m "initial commit"')
    os.chdir(current_dir)


def create_names(name):
    project_name = name.replace("_", " ").replace("-", " ").title()
    module_name = name.replace(" ", "_").replace("-", "_").lower()
    package_name = module_name.replace("_", "-")
    return project_name, module_name, package_name


def replace_names(
    content,
    project_name=None,
    module_name=None,
    package_name=None,
    git_user=None,
    git_email=None,
):
    if module_name:
        content = content.replace("{{ module_name }}", module_name)
    if package_name:
        content = content.replace("{{ package-name }}", package_name)
    if project_name:
        content = content.replace("{{ Project Name }}", project_name)
    if git_user:
        content = content.replace("{{ git_user }}", git_user)
    if git_email:
        content = content.replace("{{ git_email }}", git_email)
    return content


def create_new_project(name, path, with_react=False):
    startpath = os.getcwd()
    basepath = os.path.join(path, name)
    module_name = name.replace(" ", "_").replace("-", "_").lower()
    package_name = module_name.replace("_", "-")

    project_name, module_name, package_name = create_names(name)

    print(f"Creating project {name} at {basepath}")
    if os.path.exists(basepath) and os.path.isdir(basepath):
        # check if empty
        if os.listdir(basepath):
            print(f"Project {name} already exists")
            return
        else:
            print(f"Project {name} already exists but is empty")
            os.rmdir(basepath)

    shutil.copytree(template_path, basepath)

    # get current git user

    git_user = os.popen("git config user.name").read().strip() or "Your Name"
    git_email = (
        os.popen("git config user.email").read().strip() or "your.email@send.com"
    )

    # in each file replace "{{ project_name }}" with name
    # and "{{ git_user }}" with git_user
    # and "{{ git_email }}" with git_email
    for root, dirs, files in os.walk(basepath):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, "r") as f:
                content = f.read()
            content = replace_names(
                content,
                project_name=project_name,
                module_name=module_name,
                package_name=package_name,
                git_user=git_user,
                git_email=git_email,
            )
            with open(filepath, "w") as f:
                f.write(content)

    if not with_react:
        reactfolder = os.path.join(basepath, "react_plugin")
        shutil.rmtree(reactfolder)

    # rename the new_package folder to the project name
    os.rename(
        os.path.join(basepath, "new_package"),
        os.path.join(basepath, module_name),
    )

    # rename all files starting with "template__" by removing the "template__" prefix
    for root, dirs, files in os.walk(basepath):
        for file in files:
            if file.startswith("template__"):
                new_file = file.replace("template__", "")
                os.rename(os.path.join(root, file), os.path.join(root, new_file))
    # cd into the project folder
    os.chdir(basepath)

    # init git
    _init_git(basepath)

    os.chdir(startpath)


def update_project(path):
    # check if path is a project
    path = os.path.abspath(path)

    if not os.path.exists(path):
        raise RuntimeError(f"Path {path} does not exist")

    if not os.path.isdir(path):
        raise RuntimeError(f"Path {path} is not a directory")

    if not os.path.exists(os.path.join(path, "pyproject.toml")):
        raise RuntimeError(f"Path {path} is not a project")

    name = os.path.basename(path)
    project_name, module_name, package_name = create_names(name)

    if not os.path.exists(os.path.join(path, module_name)):
        print(f"Cant find module {module_name} in project {name}")
        return
    # check if funcnodes is in the project
    with open(os.path.join(path, "pyproject.toml")) as f:
        if "funcnodes" not in f.read():
            print(f"Project at {path} does not seem to be a funcnodes project")
            return

    for file in files_to_overwrite:
        filepath = os.path.join(path, file)
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        shutil.copy2(os.path.join(template_path, file), filepath)
        with open(filepath, "r") as f:
            content = f.read()
        content = replace_names(
            content,
            project_name=project_name,
            module_name=module_name,
            package_name=package_name,
        )
        with open(filepath, "w") as f:
            f.write(content)

    for file in files_to_copy_if_missing:
        if not os.path.exists(os.path.join(path, file)):
            filepath = os.path.join(path, file)
            if not os.path.exists(os.path.dirname(filepath)):
                os.makedirs(os.path.dirname(filepath))
            shutil.copy2(os.path.join(template_path, file), filepath)
            with open(filepath, "r") as f:
                content = f.read()
            content = replace_names(
                content,
                project_name=project_name,
                module_name=module_name,
                package_name=package_name,
            )

            with open(filepath, "w") as f:
                f.write(content)

    # update plugins in toml
    with open(os.path.join(path, "pyproject.toml")) as f:
        content = f.read()
    if '[tool.poetry.plugins."funcnodes.module"]' not in content:
        content += (
            '\n[tool.poetry.plugins."funcnodes.module"]\n'
            f'module = "{name}"\n'
            f'shelf = "{name}:NODE_SHELF"\n'
        )
        with open(os.path.join(path, "pyproject.toml"), "w") as f:
            f.write(content)

    # check if the project is already in git
    if not os.path.exists(os.path.join(path, ".git")):
        _init_git(path)
    else:
        os.system("poetry add pre-commit@* --group=dev")
        os.system("poetry add pytest@* --group=dev")
        os.system("poetry update")
        os.system("poetry run pre-commit install")
        os.system("poetry run pre-commit autoupdate")

    # check if the git branch dev and test exist
    current_dir = os.getcwd()
    os.chdir(path)
    branches = [
        s.strip().strip("*").strip()
        for s in os.popen("git branch").read().strip().split("\n")
    ]
    if "dev" not in branches:
        os.system("git reset")
        os.system("git checkout -b dev")
        os.system('git commit --allow-empty -m "initial commit"')

    if "test" not in branches:
        os.system("git reset")
        os.system("git checkout -b test")
        os.system('git commit --allow-empty -m "initial commit"')

    os.chdir(current_dir)


def main():
    argparser = argparse.ArgumentParser()

    subparsers = argparser.add_subparsers(dest="task")
    new_project_parser = subparsers.add_parser("new", help="Create a new project")

    new_project_parser.add_argument("name", help="Name of the project")
    new_project_parser.add_argument(
        "--path", help="Path to create the project", default=os.getcwd()
    )
    new_project_parser.add_argument(
        "--with_react",
        help="Add the templates for the react plugin",
        action="store_true",
    )

    update_project_parser = subparsers.add_parser(
        "update", help="Update an existing project"
    )
    update_project_parser.add_argument(
        "path", help="Path to the project", default=os.getcwd()
    )

    check_for_register_parser = subparsers.add_parser(
        "check_for_register",
        help="Check if the current project is ready for registration",
    )

    args = argparser.parse_args()

    if args.task == "new":
        create_new_project(args.name, args.path, args.with_react)
    elif args.task == "update":
        update_project(args.path)
    elif args.task == "check_for_register":
        register.check_for_register()
    else:
        print("Invalid task")


if __name__ == "__main__":
    main()
