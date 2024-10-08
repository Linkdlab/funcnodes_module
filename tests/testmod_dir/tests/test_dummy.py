import unittest
from ..testmod import node2test  # noqa E402


class DummyTest(unittest.IsolatedAsyncioTestCase):
    async def test_node2test(self):
        node2test()
        await node2test()
