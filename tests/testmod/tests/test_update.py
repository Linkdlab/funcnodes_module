import unittest
import funcnodes_module
import os


class DummyTest(unittest.IsolatedAsyncioTestCase):
    async def test_dummy(self):
        funcnodes_module.update_project(
            os.path.abspath(os.path.dirname(__file__), "..")
        )
