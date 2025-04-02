from os import system as ossystem, popen as ospopen
from .utils import chdir_context


def init_git(
    path,
):
    with chdir_context(path):
        # initialize git
        ossystem("git init")
        # create a dev and test branch
        ossystem('git commit --allow-empty -m "initial commit"')
        ossystem("git checkout -b test")
        ossystem('git commit --allow-empty -m "initial commit"')
        ossystem("git checkout -b dev")

        # # add all files

        ossystem("uv sync")
        ossystem("uv add pre-commit@* --group=dev")
        ossystem("uv add pytest@* --group=dev")
        ossystem("uv run pre-commit install")
        ossystem("uv run pre-commit autoupdate")

        ossystem("git add .")
        ossystem('git commit -m "initial commit"')


def update_git(
    path,
):
    git_path = path / ".git"
    if not git_path.exists():
        init_git(path)

    else:
        ossystem("uv sync --upgrade")
        ossystem("uv run pre-commit install")
        ossystem("uv run pre-commit autoupdate")
        try:
            ossystem("uv run pre-commit run --all-files")
        except Exception:
            pass

        with chdir_context(path):
            branches = [
                s.strip().strip("*").strip()
                for s in ospopen("git branch").read().strip().split("\n")
            ]

            if "test" not in branches:
                ossystem("git reset")
                ossystem("git checkout -b test")
                ossystem('git commit --allow-empty -m "initial commit"')

            if "dev" not in branches:
                ossystem("git reset")
                ossystem("git checkout -b dev")
                ossystem('git commit --allow-empty -m "initial commit"')
