import argparse
import os
from . import update_project, create_new_project
from .gen_licence import gen_third_party_notice


def main():
    argparser = argparse.ArgumentParser()

    subparsers = argparser.add_subparsers(dest="task")
    # subparsers.add_parser("upgrade", help="Upgrade the funcnodes-module package")
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

    update_project_parser.add_argument(
        "--force",
        help="Force overwrite of certain files",
        action="store_true",
    )

    update_project_parser.add_argument(
        "--project_name",
        help="Project name",
        default=None,
    )

    update_project_parser.add_argument(
        "--module_name",
        help="Module name",
        default=None,
    )

    update_project_parser.add_argument(
        "--package_name",
        help="Package name",
        default=None,
    )

    gen_third_party_notice_parser = subparsers.add_parser(
        "gen_third_party_notice",
        help="Generate a third party notice file",
    )

    gen_third_party_notice_parser.add_argument(
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
        update_project(
            args.path,
            nogit=args.nogit,
            force=args.force,
            project_name=args.project_name,
            module_name=args.module_name,
            package_name=args.package_name,
        )
    # elif args.task == "upgrade":
    #     # upgrades self
    #     with os.popen("pip install --upgrade funcnodes-module") as p:
    #         print(p.read())
    elif args.task == "gen_third_party_notice":
        gen_third_party_notice(args.path)
    # elif args.task == "check_for_register":
    #     register.check_for_register(args.path)
    else:
        print("Invalid task")


if __name__ == "__main__":
    main()
