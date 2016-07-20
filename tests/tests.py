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
        self.plugin_dir = os.path.join(self.test_dir, 'plug-ins')
        self.script_dir = os.path.join(self.test_dir, 'scripts')
        self.gpi_config = os.path.join(self.test_dir, '.gpi.json')

        self.maxDiff = None

        if os.path.isdir(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.isdir(self.script_dir):
            shutil.rmtree(self.script_dir)
        if os.path.isdir(self.plugin_dir):
            shutil.rmtree(self.plugin_dir)

        os.makedirs(self.plugin_dir)
        os.makedirs(self.script_dir)

        installer.gpi_config_file = self.gpi_config
        installer.gimp_config_dir = self.test_dir

        self.t = tarfile.open(
            os.path.join(self.current_dir,
                         'data', 'imguruploader.tar.gz'), 'r')
        self.manifest = json.load(self.t.extractfile('gpi.json'))

    def tearDown(self):
        shutil.rmtree(self.script_dir)
        shutil.rmtree(self.plugin_dir)
        if os.path.isfile(self.gpi_config):
            os.remove(self.gpi_config)

    def test_plugin_subdir(self):
        self.assertEqual(installer.plugin_subdir('scriptfu'),
                         os.path.join(self.test_dir, 'scripts'))
        self.assertEqual(installer.plugin_subdir('python'),
                         os.path.join(self.test_dir, 'plug-ins'))

    def test_install_different_manifest(self):
        test_manifest = self.manifest.copy()
        test_manifest['version'] = '0.2.0'
        installer.install(self.t, manifest=test_manifest)

        with open(self.gpi_config, 'r') as index:
            expected_index = {
                "packages": {
                    "imguruploader": {
                        "files": ["upload.py"],
                        "version": "0.2.0",
                        "type": "python",
                        "name": "Imgur Uploader"
                    }
                },
                "files": {
                    "upload.py": "imguruploader"
                }
            }
            self.assertEqual(json.load(index), expected_index)
        self.assertTrue(os.path.isfile(
            os.path.join(self.test_dir, 'plug-ins', 'upload.py')))

    def test_install(self):
        installer.install(self.t)

        with open(self.gpi_config, 'r') as index:
            expected_index = {
                "packages": {
                    "imguruploader": {
                        "files": ["upload.py"],
                        "version": "0.1.0",
                        "type": "python",
                        "name": "Imgur Uploader"
                    }
                },
                "files": {
                    "upload.py": "imguruploader"
                }
            }
            self.assertEqual(json.load(index), expected_index)
        self.assertTrue(os.path.isfile(
            os.path.join(self.test_dir, 'plug-ins', 'upload.py')))

    def test_install_scriptfu(self):
        t = tarfile.open(
            os.path.join(self.current_dir,
                         'data', 'imguruploader-scriptfu.tar.gz'), 'r')
        installer.install(t)

        with open(self.gpi_config, 'r') as index:
            expected_index = {
                "packages": {
                    "imguruploader": {
                        "files": ["upload.scm"],
                        "version": "0.1.0",
                        "type": "scriptfu",
                        "name": "Imgur Uploader"
                    }
                },
                "files": {
                    "upload.scm": "imguruploader"
                }
            }
            self.assertEqual(json.load(index), expected_index)
        self.assertTrue(os.path.isfile(
            os.path.join(self.test_dir, 'scripts', 'upload.scm')))

    def test_uninstall(self):
        t = tarfile.open(
            os.path.join(self.current_dir,
                         'data', 'imguruploader-scriptfu.tar.gz'), 'r')
        installer.install(t)

        uninstall_success = installer.uninstall('imguruploader')
        self.assertFalse(os.path.isfile(
            os.path.join(self.test_dir, 'scripts', 'upload.py')))
        self.assertTrue(uninstall_success)

    def test_uninstall_dirs(self):
        t1 = tarfile.open(
            os.path.join(self.current_dir, 'data', 'dir1.tar.gz'), 'r')
        t2 = tarfile.open(
            os.path.join(self.current_dir, 'data', 'dir2.tar.gz'), 'r')
        installer.install(t1)
        installer.install(t2)
        uninstall_success = installer.uninstall('containsdir1')

        # biz and its sub-dirs and files are only written by dir1
        self.assertFalse(os.path.isdir(
            os.path.join(self.test_dir, 'plug-ins', 'biz')))

        # foo/ is written by dir1 and dir2, but foo/baz is only written by dir1
        self.assertFalse(os.path.isdir(
            os.path.join(self.test_dir, 'plug-ins', 'foo', 'baz')))
        self.assertTrue(uninstall_success)

    def test_uninstall_scriptfu(self):
        installer.install(self.t)
        uninstall_success = installer.uninstall('imguruploader')
        self.assertFalse(os.path.isfile(
            os.path.join(self.test_dir, 'plug-ins', 'upload.py')))
        self.assertTrue(uninstall_success)

    def test_uninstall_nonexistent(self):
        uninstall_success = installer.uninstall('nonexistent')
        self.assertFalse(uninstall_success)

    def test_info_local(self):
        installer.install(self.t)
        with open(self.gpi_config, 'r') as index:
            self.assertEqual(
                installer.local_info(
                    'imguruploader',
                    json.load(index)['packages']['imguruploader']),
                {
                    'installed': True,
                    'version': '0.1.0',
                    'description': None,
                    'name': 'imguruploader'
                })

    def test_info_remote(self):
        self.assertEqual(
            installer.remote_info('exportlayers'),
            {
                'name': 'exportlayers',
                'versions_available': [{
                    'version': "2.3.0",
                    'file': '/uploads/exportlayers/2.3.0/'
                            'exportlayers-2.3.0.tar.gz'
                }],
                'description': None,
                'installed': False
            })

    def test_info(self):
        self.assertEqual(
            installer.remote_info('imguruploader'),
            {
                'name': 'imguruploader',
                'versions_available': [{
                    'version': "0.1.1",
                    'file': '/uploads/imguruploader/0.1.1/'
                    'imguruploader-0.1.1.tar.gz'
                    },
                    {
                    'version': "0.1.0",
                    'file': '/uploads/imguruploader/0.1.0/'
                    'imguruploader-0.1.0.tar_nJzegdA.gz'
                }],
                'description': None,
                'installed': False
            })
        installer.install(self.t)
        with open(self.gpi_config, 'r') as index:
            self.assertEqual(
                installer.local_info(
                    'imguruploader',
                    json.load(index)['packages']['imguruploader']),
                {
                    'installed': True,
                    'version': '0.1.0',
                    'description': None,
                    'name': 'imguruploader'
                })

    def test_currently_installed(self):
        installer.install(self.t)
        self.assertEqual(installer.currently_installed(),
                         [{'name': 'Imgur Uploader', 'version': '0.1.0'}])

    def test_overlapping_files_fatal(self):
        # package1 and package2 both contain the file contents/file.py, with
        # different contents. The installer should return a fatal error.
        package1 = tarfile.open(
            os.path.join(self.current_dir,
                         'data', 'overlappingfiles1.tar.gz'), 'r')
        package2 = tarfile.open(
            os.path.join(self.current_dir,
                         'data', 'overlappingfiles2.tar.gz'), 'r')
        installer.install(package1)
        with self.assertRaises(Exception):
            installer.install(package2)

        self.assertEqual(installer.currently_installed(),
                         [{'name': 'Overlapping Files 1', 'version': '0.1.0'}])
