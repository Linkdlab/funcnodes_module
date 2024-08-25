import unittest
import os
import tempfile

from funcnodes_module import (
    create_new_project,
    update_project,
)

from funcnodes_module.config import (
    files_to_copy_if_missing,
    files_to_overwrite,
    template_path,
)


class TestMod(unittest.TestCase):
    def _check_files(self):
        for file in files_to_copy_if_missing + files_to_overwrite:
            self.assertTrue(
                os.path.exists(os.path.join(template_path, file)),
                f"File {file} not found",
            )

    def test_mod(self):
        odir = os.getcwd()
        self._check_files()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(tmpdir)
                self.assertFalse(os.path.exists("dummy_module"))

                create_new_project("dummy_module", tmpdir)

                self.assertTrue(os.path.exists("dummy_module"))
                os.chdir("dummy_module")
                update_project(".")
            finally:
                os.chdir(odir)  # Ensure you return to the original directory
