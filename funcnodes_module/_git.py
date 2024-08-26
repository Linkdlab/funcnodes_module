import os


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
