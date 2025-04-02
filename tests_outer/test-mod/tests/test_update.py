import funcnodes_module
from pathlib import Path
import sys

print(sys.path)


def test_update():
    funcnodes_module.update_project(Path(__file__).parent.parent.absolute(), nogit=True)


# def test_build():
#     with chdir_context(Path(__file__).parent.parent.absolute()):
#         os.system("uv build --all --no-cache-dir")
