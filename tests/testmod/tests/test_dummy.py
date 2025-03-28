from pytest_funcnodes import nodetest
from testmod import node2test  # noqa E402


@nodetest(node2test)
async def test_node2test():
    node2test()
    await node2test()
