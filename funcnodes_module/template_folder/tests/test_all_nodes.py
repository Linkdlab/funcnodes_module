import sys
import os

sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)  # in case test folder is not in sys path

from all_nodes_test_base import TestAllNodesBase
from typing import List
import unittest
import funcnodes as fn
import {{ module_name }} as fnmodule



class TestAllNodes(TestAllNodesBase):
    ### in this test class all nodes should be triggered at least once to mark them as testing
    sub_test_classes: List[unittest.IsolatedAsyncioTestCase] = []

    async def test_first_node(self):
        node = fnmodule.FirstNode()
        node.inputs["x"].value = "foo"
        await node
        self.assertEqual(node.get_output("out").value, "bar")
