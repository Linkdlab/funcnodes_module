import unittest
import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)  # in case test folder is not in sys path
from testmod import node2test  # noqa E402


class DummyTest(unittest.IsolatedAsyncioTestCase):
    async def test_node2test(self):
        node2test()
        await node2test()
