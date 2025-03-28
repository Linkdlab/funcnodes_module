from pytest_funcnodes import all_nodes_tested
import testmod as fnmodule  # noqa


def test_all_nodes_tested(all_nodes):
    all_nodes_tested(all_nodes, fnmodule.NODE_SHELF, ignore=[fnmodule.node2ignore])
