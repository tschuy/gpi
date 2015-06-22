import os
import json
import shutil
import tarfile
import unittest

from gpi import installer, web

class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.test_dir = os.path.join(self.current_dir, 'testdir')
        os.makedirs(self.test_dir)

        installer.gpi_config_file = os.path.join(self.test_dir, '.gpi.json')
        installer.gimp_plugins_dir = self.test_dir

    def tearDown(self):
        shutil.rmtree(self.test_dir)


    def test_install(self):
        t = tarfile.open(os.path.join(self.current_dir,
            'data', 'imguruploader.tar.gz'), 'r')
        manifest = json.load(t.extractfile('gpi.json'))

        installer.install(t, manifest)

        with open(os.path.join(self.test_dir, '.gpi.json'), 'r') as index:
            expected_index = {"imguruploader": {
                                  "files": ["upload.py"],
                                  "version": "0.1.0",
                                  "name": "Imgur Uploader"}}
            self.assertEqual(json.load(index), expected_index)
        self.assertTrue(os.path.isfile(
            os.path.join(self.test_dir, '.gpi.json')))
