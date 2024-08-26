import sys
import os

sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)  # in case test folder is not in sys path

from all_nodes_test_base import TestAllNodesBase
from .test_dummy import DummyTest


class TestAllNodes(TestAllNodesBase):
    sub_test_classes = [DummyTest]

    