import unittest
import tempfile
import os
from pathlib import Path
from funcnodes_module import create_new_project, update_project
from funcnodes_module.utils import (
    chdir_context,
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
                (template_path / file).exists(),
                f"File {file} not found",
            )

    def test_mod(self):
        self._check_files()

        with tempfile.TemporaryDirectory() as tmpdir:
            with chdir_context(tmpdir):
                dummy_module_path = Path("dummy_module")
                self.assertFalse(dummy_module_path.exists())

                create_new_project("dummy_module", tmpdir)

                self.assertTrue(dummy_module_path.exists())
                update_project(dummy_module_path)

                # test build
                buildpath = (dummy_module_path / "dist").absolute()
                with chdir_context(dummy_module_path):
                    print("Current directory: ", os.getcwd())
                    self.assertFalse(buildpath.exists())
                    os.system("uv build --no-cache-dir")
                    self.assertTrue(
                        buildpath.exists(),
                        f"'dist' not found only {list(Path('.').iterdir())}",
                    )
