from pathlib import Path
from typing import List

template_path = Path(__file__).parent / "template_folder"
files_to_overwrite: List[Path] = [
    Path(".github", "workflows", "py_test.yml"),
    Path(".github", "workflows", "version_publish_main.yml"),
    Path(".github", "actions", "install_package", "action.yml"),
]

files_to_copy_if_missing: List[Path] = [
    Path("tests", "test_all_nodes_pytest.py"),
    Path(".pre-commit-config.yaml"),
    Path(".flake8"),
    Path("MANIFEST.in"),
    Path("pytest.ini"),
]

files_to_overwrite_on_force: List[Path] = [
    Path(".pre-commit-config.yaml"),
    Path(".flake8"),
]


package_requirements: List[str] = [
    "funcnodes",
]

dev_requirements: List[str] = [
    "pre-commit",
    "pytest",
    "funcnodes-module",
    "pytest_funcnodes",
]

gitpaths: List[str] = [
    ".github",
    ".git",
]
