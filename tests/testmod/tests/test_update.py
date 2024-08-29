import unittest
import funcnodes_module
import os


class UpdateTest(unittest.IsolatedAsyncioTestCase):
    async def test_update(self):
        funcnodes_module.update_project(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), nogit=True
        )
