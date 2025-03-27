import argparse
import os
from . import update_project, create_new_project
from .gen_licence import gen_third_party_notice
import asyncio
import subprocess_monitor
from pathlib import Path


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

    from funcnodes_core import config

    config.reload(funcnodes_config_dir=str(Path(".funcnodes").absolute()))

    spm = subprocess_monitor.SubprocessMonitor()

    spm_task = asyncio.create_task(spm.run())

    demoworker_path = Path(".funcnodes") / "workers" / "worker_demoworker"
    if (
        not demoworker_path.exists()
        or not (demoworker_path.parent / "worker_demoworker.json").exists()
    ):
        res = await subprocess_monitor.send_spawn_request(
            command="uv",
            args=[
                "run",
                "funcnodes",
                "--dir",
                ".funcnodes",
                "worker",
                "--uuid",
                "demoworker",
                "new",
                "--not-in-venv",
                "--create-only",
            ],
            host=spm.host,
            port=spm.port,
        )
        createworkerpid = res["pid"]
        await asyncio.sleep(1)
        while createworkerpid in spm.process_ownership:
            await asyncio.sleep(1)

    res = await subprocess_monitor.send_spawn_request(
        command="uv",
        args=[
            "run",
            "funcnodes",
            "--dir",
            ".funcnodes",
            "worker",
            "--uuid",
            "demoworker",
            "start",
        ],
        host=spm.host,
        port=spm.port,
    )
    startworkerpid = res["pid"]

    res = await subprocess_monitor.send_spawn_request(
        command="uv",
        args=[
            "run",
            "funcnodes",
            "--dir",
            ".funcnodes",
            "runserver",
        ],
        host=spm.host,
        port=spm.port,
    )
    startserverpid = res["pid"]

    asyncio.create_task(
        subprocess_monitor.subscribe(
            pid=startworkerpid,
            host=spm.host,
            port=spm.port,
            callback=lambda data: print("Worker >>", data["data"]),
        )
    )

    asyncio.create_task(
        subprocess_monitor.subscribe(
            pid=startserverpid,
            host=spm.host,
            port=spm.port,
            callback=lambda data: print("Server >>", data["data"]),
        )
    )

    try:
        while True:
            await asyncio.sleep(10)
    except KeyboardInterrupt:
        pass

    spm.stop_serve()
    print("Stopped server")
    await spm_task
    print("Stopped monitor")

    await asyncio.sleep(2)


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

    demoworker_parser.add_argument(
        "--no-build",
        help="Skip building the project",
        action="store_true",
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
        os.system("uv sync --upgrade")
        if not args.no_build:
            os.system("uv build")
        asyncio.run(run_demo_worker())

    else:
        print("Invalid task")


if __name__ == "__main__":
    main()
