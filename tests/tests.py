import os
import json
import shutil
import tarfile
import unittest

from gpi import installer


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.test_dir = os.path.join(self.current_dir, 'testdir')
        if os.path.isdir(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)

        installer.gpi_config_file = os.path.join(self.test_dir, '.gpi.json')
        installer.gimp_plugins_dir = self.test_dir

        self.t = tarfile.open(
            os.path.join(self.current_dir,
                         'data', 'imguruploader.tar.gz'), 'r')
        self.manifest = json.load(self.t.extractfile('gpi.json'))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_install(self):
        installer.install(self.t, self.manifest)

        with open(os.path.join(self.test_dir, '.gpi.json'), 'r') as index:
            expected_index = {
                "imguruploader": {
                    "files": ["upload.py"],
                    "version": "0.1.0",
                    "name": "Imgur Uploader"}
                }
            self.assertEqual(json.load(index), expected_index)
        self.assertTrue(os.path.isfile(
            os.path.join(self.test_dir, 'upload.py')))

    def test_uninstall(self):
        installer.install(self.t, self.manifest)
        uninstall_success = installer.uninstall('imguruploader')
        self.assertFalse(os.path.isfile(
            os.path.join(self.test_dir, 'upload.py')))
        self.assertTrue(uninstall_success)

    def test_uninstall_nonexistent(self):
        uninstall_success = installer.uninstall('nonexistent')
        self.assertFalse(uninstall_success)
