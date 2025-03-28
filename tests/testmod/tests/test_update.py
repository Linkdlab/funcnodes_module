import pytest
import funcnodes_module
import os

import sys

print(sys.path)


@pytest.mark.asyncio
async def test_update():
    funcnodes_module.update_project(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), nogit=True
    )
