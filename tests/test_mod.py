import unittest
import os
import tempfile

from funcnodes_module.__main__ import create_new_project


class TestMod(unittest.TestCase):
    def test_mod(self):
        odir = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                self.assertFalse(os.path.exists("dummy_module"))

                create_new_project("dummy_module", tmpdir)

                self.assertTrue(os.path.exists("dummy_module"))
            finally:
                os.chdir(odir)  # Ensure you return to the original directory
