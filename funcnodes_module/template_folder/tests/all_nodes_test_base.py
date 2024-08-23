# this is an autogenerated file, do not edit it directly or your changes might be lost.
import unittest
from {{ project_name }} import NODE_SHELF


class TestAllNodesBase(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        def get_all_nodes_classes(shelf, current=None):
            if current is None:
                current = []
            if "nodes" in shelf:
                for node in shelf["nodes"]:
                    if node not in current:
                        current.append(node)

            if "subshelves" in shelf:
                for subshelf in shelf["subshelves"]:
                    get_all_nodes_classes(subshelf, current)

            return current

        all_nodes = get_all_nodes_classes(NODE_SHELF)
        nodes_to_test = all_nodes.copy()

        # monkey patching the async func method in the nodeclasses that if they are called the nodeclass is removed from the NODES_TO_TEST list
        def monkey_patch_func(node_class):
            ofunc = node_class.func
            node_class.TestAllNodes_func = ofunc

            async def func(self, *args, **kwargs):
                res = await ofunc(self, *args, **kwargs)
                if node_class in nodes_to_test:
                    nodes_to_test.remove(node_class)
                return res

            node_class.func = func

        for node_class in all_nodes:
            monkey_patch_func(node_class)

        cls.all_nodes = all_nodes
        cls.nodes_to_test = nodes_to_test

    @classmethod
    def tearDownClass(cls):
        # undo the monkey patching
        for node_class in cls.all_nodes:
            if hasattr(node_class, "TestAllNodes_func"):
                node_class.func = node_class.TestAllNodes_func
                del node_class.TestAllNodes_func

        # Final assertion to ensure all nodes were tested
        if cls.nodes_to_test:
            raise AssertionError(f"These nodes were not tested ({ len(cls.nodes_to_test) }): { cls.nodes_to_test}")
