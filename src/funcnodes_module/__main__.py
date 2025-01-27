import argparse
import os
from . import update_project, create_new_project
from .gen_licence import gen_third_party_notice
import asyncio


async def run_command(cmd, name, terminate_event):
    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    print(f"{name} started with PID: {process.pid}")

    try:
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            print(f"{name} failed with exit code {process.returncode}")
            print(stderr.decode())
            terminate_event.set()  # Signal termination
        else:
            print(f"{name} completed successfully.")
    finally:
        return process


async def run_demo_worker():
    # Termination event to signal processes to stop
    server_terminate_event = asyncio.Event()
    worker_started_event = asyncio.Event()

    # Run both commands concurrently
    server_task = asyncio.create_task(
        run_command(
            ["uv", "run", "funcnodes", "--dir", ".funcnodes", "runserver"],
            "Server",
            server_terminate_event,
        )
    )
    worker_task_start = asyncio.create_task(
        run_command(
            [
                "uv",
                "run",
                "funcnodes",
                "--dir",
                ".funcnodes",
                "worker",
                "--uuid",
                "demoworker",
                "start",
            ],
            "Worker",
            worker_started_event,
        )
    )

    processes = [server_task, worker_task_start]

    # Wait for any command to fail or complete
    done, pending = await asyncio.wait(
        [server_task, worker_task_start], return_when=asyncio.FIRST_COMPLETED
    )

    if worker_started_event.is_set() and not server_terminate_event.is_set():
        worker_started_event.clear()
        worker_task_start = asyncio.create_task(
            run_command(
                [
                    "uv",
                    "run",
                    "funcnodes",
                    "--dir",
                    ".funcnodes",
                    "worker",
                    "--uuid",
                    "demoworker",
                    "new",
                    "--create-only",
                    "--not-in-venv",
                ],
                "Worker",
                worker_started_event,
            )
        )
        processes.append(worker_task_start)
        done, pending = await asyncio.wait(
            list(pending) + [worker_task_start], return_when=asyncio.FIRST_COMPLETED
        )

    # Cancel any remaining tasks
    for task in pending:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    # Wait for all tasks to finish properly
    await asyncio.gather(*processes, return_exceptions=True)


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

    demoworker_parser = subparsers.add_parser(  # noqa F841
        "demoworker",
        help="Generate and run a demo worker",
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
    elif args.task == "demoworker":
        # os.system("uv sync --upgrade")
        # os.system("uv build")
        asyncio.run(run_demo_worker())

    else:
        print("Invalid task")


if __name__ == "__main__":
    main()
