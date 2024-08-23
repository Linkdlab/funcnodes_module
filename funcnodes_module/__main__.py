import argparse
import os
import shutil


def create_new_project(name, path, with_react=False):
    basepath = os.path.join(path, name)
    print(f"Creating project {name} at {basepath}")
    if os.path.exists(basepath) and os.path.isdir(basepath):
        # check if empty
        if os.listdir(basepath):
            print(f"Project {name} already exists")
            return
        else:
            print(f"Project {name} already exists but is empty")
            os.rmdir(basepath)

    template_path = os.path.join(os.path.dirname(__file__), "template_folder")
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
            content = content.replace("{{ project_name }}", name)
            content = content.replace(
                "{{ Project Name }}", name.replace("_", " ").title()
            )
            content = content.replace("{{ git_user }}", git_user)
            content = content.replace("{{ git_email }}", git_email)
            with open(filepath, "w") as f:
                f.write(content)

    if not with_react:
        reactfolder = os.path.join(basepath, "react_plugin")
        shutil.rmtree(reactfolder)

    # rename the new_package folder to the project name
    os.rename(os.path.join(basepath, "new_package"), os.path.join(basepath, name))

    # rename all files starting with "template__" by removing the "template__" prefix
    for root, dirs, files in os.walk(basepath):
        for file in files:
            if file.startswith("template__"):
                new_file = file.replace("template__", "")
                os.rename(os.path.join(root, file), os.path.join(root, new_file))
    # cd into the project folder
    os.chdir(basepath)

    # initialize git
    os.system("git init")
    os.system('git commit --allow-empty -m "initial commit"')
    # create a dev and test branch
    os.system("git checkout -b test")
    os.system('git commit --allow-empty -m "initial commit"')
    os.system("git checkout -b dev")

    # # add all files

    os.system("poetry install")
    os.system("poetry run pre-commit install")
    os.system("poetry run pre-commit autoupdate")

    os.system("git add .")
    os.system('git commit -m "initial commit"')


def update_project(path):
    # check if path is a project
    if not os.path.exists(path):
        print(f"Path {path} does not exist")
        return

    if not os.path.isdir(path):
        print(f"Path {path} is not a directory")
        return

    if not os.path.exists(os.path.join(path, "pyproject.toml")):
        print(f"Path {path} is not a project")
        return
    path = os.path.abspath(path)
    name = os.path.basename(path)
    # check if funcnodes is in the project
    with open(os.path.join(path, "pyproject.toml")) as f:
        if "funcnodes" not in f.read():
            print(f"Project at {path} does not seem to be a funcnodes project")
            return

    template_path = os.path.join(os.path.dirname(__file__), "template_folder")
    files_to_overwrite = [
        os.path.join(".github", "workflows", "funcnodes_module_wf.yaml"),
        os.path.join("tests", "all_nodes_test_base.py"),
    ]
    for file in files_to_overwrite:
        filepath = os.path.join(path, file)
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        shutil.copy2(os.path.join(template_path, file), filepath)
        with open(filepath, "r") as f:
            content = f.read()
        content = content.replace("{{ project_name }}", name)
        content = content.replace("{{ Project Name }}", name.replace("_", " ").title())
        with open(filepath, "w") as f:
            f.write(content)

    files_to_copy_if_missing = [
        os.path.join("tests", "test_all_nodes.py"),
        os.path.join(".pre-commit-config.yaml"),
    ]
    for file in files_to_copy_if_missing:
        if not os.path.exists(os.path.join(path, file)):
            filepath = os.path.join(path, file)
            if not os.path.exists(os.path.dirname(filepath)):
                os.makedirs(os.path.dirname(filepath))
            shutil.copy2(os.path.join(template_path, file), filepath)
            with open(filepath, "r") as f:
                content = f.read()
            content = content.replace("{{ project_name }}", name)
            content = content.replace(
                "{{ Project Name }}", name.replace("_", " ").title()
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

    os.system("poetry add pre-commit@* --group=dev")
    os.system("poetry add pytest@* --group=dev")
    os.system("poetry update")
    os.system("poetry run pre-commit install")
    os.system("poetry run pre-commit autoupdate")


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

    args = argparser.parse_args()

    if args.task == "new":
        create_new_project(args.name, args.path, args.with_react)
    elif args.task == "update":
        update_project(args.path)
    else:
        print("Invalid task")


if __name__ == "__main__":
    main()
