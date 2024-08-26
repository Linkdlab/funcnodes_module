import argparse
import os
from . import register, update_project, create_new_project


def main():
    argparser = argparse.ArgumentParser()

    subparsers = argparser.add_subparsers(dest="task")
    new_project_parser = subparsers.add_parser("new", help="Create a new project")

    new_project_parser.add_argument("name", help="Name of the project")

    new_project_parser.add_argument(
        "--with_react",
        help="Add the templates for the react plugin",
        action="store_true",
    )

    new_project_parser.add_argument(
        "--nogit",
        help="Skip the git part of the project creation/update",
        action="store_true",
    )

    new_project_parser.add_argument(
        "--path",
        help="Project path",
        default=os.getcwd(),
    )

    update_project_parser = subparsers.add_parser(
        "update", help="Update an existing project"
    )

    update_project_parser.add_argument(
        "--with_react",
        help="Add the templates for the react plugin",
        action="store_true",
    )

    update_project_parser.add_argument(
        "--nogit",
        help="Skip the git part of the project creation/update",
        action="store_true",
    )

    update_project_parser.add_argument(
        "--path",
        help="Project path",
        default=os.getcwd(),
    )

    # check_for_register_parser = subparsers.add_parser(
    #     "check_for_register",
    #     help="Check if the current project is ready for registration",
    # )

    args = argparser.parse_args()

    if args.task == "new":
        create_new_project(args.name, args.path, args.with_react, nogit=args.nogit)
    elif args.task == "update":
        update_project(args.path, nogit=args.nogit)
    # elif args.task == "check_for_register":
    #     register.check_for_register(args.path)
    else:
        print("Invalid task")


if __name__ == "__main__":
    main()
