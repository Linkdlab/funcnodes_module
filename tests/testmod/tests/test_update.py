import pytest
import funcnodes_module
from pathlib import Path
import sys

print(sys.path)


@pytest.mark.asyncio
async def test_update():
    funcnodes_module.update_project(Path(__file__).parent.parent.absolute(), nogit=True)
