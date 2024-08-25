import argparse
import os
from . import register, update_project, create_new_project


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

    check_for_register_parser.add_argument(
        "--path", help="Path to the project", default=os.getcwd()
    )

    args = argparser.parse_args()

    if args.task == "new":
        create_new_project(args.name, args.path, args.with_react)
    elif args.task == "update":
        update_project(args.path)
    elif args.task == "check_for_register":
        register.check_for_register(args.path)
    else:
        print("Invalid task")


if __name__ == "__main__":
    main()
