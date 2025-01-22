import os
import shutil
import toml
from .utils import create_names, replace_names, read_file_content, write_file_content
from .config import (
    template_path,
    files_to_overwrite,
    files_to_copy_if_missing,
    files_to_overwrite_on_force,
    dev_requirements,
    package_requirements,
)
from ._git import _init_git


def package_name_version_to_name(name, version):
    if not version or version == "*":
        return name
    if version.startswith("^"):
        return f"{name}>={version[1:]}"
    if version.startswith("~"):
        return f"{name}>={version[1:]},<{version[1:]}.*"
    if version[0].isdigit():
        return f"{name}=={version}"
    return f"{name}{version}"


def update_toml(path, module_name):
    with open(path, "r") as f:
        tomldata = toml.load(f)

    o_dump = toml.dumps(tomldata)

    if "tool" not in tomldata:
        tomldata["tool"] = {}

    tool = tomldata["tool"]

    if "project" not in tomldata:
        if "poetry" in tool:
            tomldata["project"] = tool["poetry"]
            del tool["poetry"]

    project = tomldata["project"]
    if "license" in project:
        if isinstance(project["license"], str):
            project["license"] = {"text": project["license"]}

    # update poetry remaining entry points
    if "plugins" in project:
        if "funcnodes.module" in project["plugins"]:
            if "entry-points" not in project:
                project["entry-points"] = {}
            project["entry-points"]["funcnodes.module"] = project["plugins"][
                "funcnodes.module"
            ]
            del project["plugins"]["funcnodes.module"]

    if "entry-points" not in project:
        project["entry-points"] = {}

    entry_points = project["entry-points"]

    if "funcnodes.module" not in entry_points:
        entry_points["funcnodes.module"] = {}

    fnm = entry_points["funcnodes.module"]

    if "module" not in fnm:
        fnm["module"] = module_name

    if "shelf" not in fnm:
        fnm["shelf"] = f"{module_name}:NODE_SHELF"

    if "setuptools" not in tool:
        tool["setuptools"] = {}

    setuptools = tool["setuptools"]

    if "packages" not in setuptools:
        setuptools["packages"] = {"find": {"where": ["src"]}}

    if "package-dir" not in setuptools:
        setuptools["package-dir"] = {"": "src"}

    # update remaining poetry [tool.poetry.group.dev.dependencies]
    if "group" in project:
        if "dev" in project["group"]:
            if "dependencies" in project["group"]["dev"]:
                dev = project["group"]["dev"]["dependencies"]

                if "dependency-groups" not in project:
                    project["dependency-groups"] = {}

                project["dependency-groups"]["dev"] = [
                    package_name_version_to_name(k, v) for k, v in dev.items()
                ]

    if "dependencies" in project:
        if isinstance(project["dependencies"], dict):
            project["dependencies"] = [
                package_name_version_to_name(k, v)
                for k, v in project["dependencies"].items()
            ]

    n_dump = toml.dumps(tomldata)

    if o_dump != n_dump:
        with open(path, "w") as f:
            toml.dump(tomldata, f)


def update_project(
    path,
    nogit=False,
    force=False,
    project_name=None,
    module_name=None,
    package_name=None,
):
    # check if path is a project
    path = os.path.abspath(path)

    if not os.path.exists(path):
        raise RuntimeError(f"Path {path} does not exist")

    if not os.path.isdir(path):
        raise RuntimeError(f"Path {path} is not a directory")

    if not os.path.exists(os.path.join(path, "pyproject.toml")):
        raise RuntimeError(f"Path {path} is not a project")

    os.system("python -m pip install uv --upgrade")

    name = os.path.basename(path)
    _project_name, _module_name, _package_name = create_names(name)

    project_name = project_name or _project_name
    module_name = module_name or _module_name
    package_name = package_name or _package_name

    if not os.path.exists(os.path.join(path, "src", module_name)):
        if os.path.exists(os.path.join(path, module_name)):
            if not os.path.exists(os.path.join(path, "src")):
                os.makedirs(os.path.join(path, "src"))
            os.rename(
                os.path.join(path, module_name), os.path.join(path, "src", module_name)
            )
        else:
            print(f"Can't find module {module_name} in project {name}")
            return
    # check if funcnodes is in the project

    content, _ = read_file_content(os.path.join(path, "pyproject.toml"))
    if "funcnodes" not in content:
        print(f"Project at {path} does not seem to be a funcnodes project")
        return

    f2over = files_to_overwrite
    if force:
        f2over += files_to_overwrite_on_force

    for file in f2over:
        filepath = os.path.join(path, file)
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        shutil.copy2(os.path.join(template_path, file), filepath)
        content, enc = read_file_content(filepath)

        content = replace_names(
            content,
            project_name=project_name,
            module_name=module_name,
            package_name=package_name,
        )
        write_file_content(filepath, content, enc)

    for file in files_to_copy_if_missing:
        if not os.path.exists(os.path.join(path, file)):
            filepath = os.path.join(path, file)
            if not os.path.exists(os.path.dirname(filepath)):
                os.makedirs(os.path.dirname(filepath))
            shutil.copy2(os.path.join(template_path, file), filepath)
            content, enc = read_file_content(filepath)
            content = replace_names(
                content,
                project_name=project_name,
                module_name=module_name,
                package_name=package_name,
            )
            write_file_content(filepath, content, enc)

    # update requirements
    os.system(f"uv add {' '.join(dev_requirements)} --group dev")
    os.system(f"uv add {' '.join(package_requirements)}")

    # update plugins in toml
    update_toml(os.path.join(path, "pyproject.toml"), module_name=module_name)

    # check if the project is already in git
    if not os.path.exists(os.path.join(path, ".git")) and not nogit:
        _init_git(path)
    else:
        os.system("uv sync --upgrade")
        if not nogit:
            os.system("uv run pre-commit install")
            os.system("uv run pre-commit autoupdate")
            try:
                os.system("uv run pre-commit run --all-files")
            except Exception:
                pass

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
