import json
import os
import sys

from gpi.web import get_package_info

# FIXME: Add a sane default path for Windows.
if sys.platform == 'darwin':
    default_config_dir = os.path.expanduser(
        '~/Library/Application Support/GIMP/2.8/'
    )
elif sys.platform.startswith('linux'):
    default_config_dir = os.path.expanduser('~/.gimp-2.8/')
else:
    default_config_dir = os.path.expanduser('~/.gimp-2.8/')

gimp_config_dir = os.environ.get(
    'GIMP_CONFIG_DIR', default_config_dir)

gpi_config_file = os.path.join(gimp_config_dir, '.gpi.json')

verbose = False


def is_non_zero_file(path):
    return True if os.path.isfile(
        path) and os.path.getsize(path) > 0 else False


def plugin_subdir(plugin_type):
    if plugin_type == 'scriptfu':
        return os.path.join(gimp_config_dir, 'scripts')
    else:
        return os.path.join(gimp_config_dir, 'plug-ins')


def install(tar, manifest=None):
    if manifest is None:
        manifest = json.load(tar.extractfile('gpi.json'))

    if not is_non_zero_file(gpi_config_file):
        index = {}
    else:
        with open(gpi_config_file, 'r') as f:
            index = json.load(f)

    directory = plugin_subdir(manifest.get('type', 'python'))

    files = [t for t in tar if t.name.startswith("contents/")]

    for t in files:
        t.name = t.name[9:]  # contents/
        if verbose:
            print "Installing {} to {}/{}".format(
                t.name, directory, t.name)

    plugin_info = {
        'version': manifest['version'],
        'name': manifest['name'],
        'files': [file.name for file in files],
        'type': manifest.get('type', 'python')
    }
    index[manifest['identifier']] = plugin_info

    with open(gpi_config_file, 'w+') as f:
        f.write(json.dumps(index))

    tar.extractall(directory, members=files)


def uninstall(plugin_name):
    if not os.path.isfile(gpi_config_file):
        return False
    with open(gpi_config_file, 'r') as f:
        index = json.load(f)
        if plugin_name not in index:
            return False

    directory = plugin_subdir(index[plugin_name]['type'])
    directories = []
    for file in index[plugin_name]['files']:
        # TODO remove empty directories
        full_path = os.path.join(directory, file)
        if os.path.isdir(full_path):
            directories.append(full_path)
        else:
            os.remove(full_path)

    del index[plugin_name]
    with open(gpi_config_file, 'w') as f:
        f.write(json.dumps(index))

    return True


def info(plugin_name):
    """Lists all installed packages registered with gpi.
    Always lists the package name and whether it is installed.
    If the package is installed the installed version is listed.
    If the package is not installed the available versions are listed.
    If there is a package description, print that too.
    """
    # Note that we rely on the API giving us a dictionary with a 'releases' key
    # which holds a list of dictionaries, each containing a 'version' key.
    # We rely on the package in the GPI config file to have a 'version' key.

    # Handle the case where the config file doesn't exist. This may happen if
    # nothing has been installed before.
    if os.path.isfile(gpi_config_file):
        with open(gpi_config_file, 'r') as f:
            index = json.load(f)
        if plugin_name in index:
            return local_info(plugin_name, index[plugin_name])
    return remote_info(plugin_name)


def local_info(plugin_name, plugin_metadata):
    """Return info about an installed package as a dict"""
    return dict(
        name=plugin_name,
        description=plugin_metadata.get('description'),
        version=plugin_metadata['version'],
        installed=True)


def remote_info(plugin_name):
    """Return human readable info about a package which is not installed.
    Fetches info from the server.

    Will raise a PackageNotFound exception if the package doesn't exist
    locally or remotely."""
    plugin_info = get_package_info(plugin_name)
    return dict(
        name=plugin_name,
        description=plugin_info.get('description'),
        versions_available=plugin_info['releases'],
        installed=False)


def currently_installed():
    if os.path.isfile(gpi_config_file):
        with open(gpi_config_file, 'r') as f:
            index = json.load(f)
        return [
            {'name': index[i]['name'], 'version': index[i]['version']}
            for i in index]
    else:
        return []
