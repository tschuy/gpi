import json
import os
import sys

from gpi.web import get_package_info, PackageNotFound

# FIXME: Add a sane default path for Windows.
if sys.platform == 'darwin':
    default_plugins_dir = os.path.expanduser(
        '~/Library/Application Support/GIMP/2.8/plug-ins/'
    )
elif sys.platform.startswith('linux'):
    default_plugins_dir = os.path.expanduser('~/.gimp-2.8/plug-ins/')
else:
    default_plugins_dir = os.path.expanduser('~/.gimp-2.8/plug-ins/')

gimp_plugins_dir = os.environ.get(
    'GIMP_PLUGIN_DIR', default_plugins_dir)

gpi_config_file = os.path.join(gimp_plugins_dir, '.gpi.json')

verbose = False


def is_non_zero_file(path):
    return True if os.path.isfile(
        path) and os.path.getsize(path) > 0 else False


def install(tar, manifest):
    if not is_non_zero_file(gpi_config_file):
        index = {}
    else:
        with open(gpi_config_file, 'r') as f:
            index = json.load(f)

    files = [t for t in tar if t.name.startswith("contents/")]

    for t in files:
        t.name = t.name[9:]  # contents/
        if verbose:
            print "Installing {} to {}/{}".format(
                t.name, gimp_plugins_dir, t.name)

    plugin_info = {
        'version': manifest['version'],
        'name': manifest['name'],
        'files': [file.name for file in files]
    }
    index[manifest['identifier']] = plugin_info

    with open(gpi_config_file, 'w') as f:
        f.write(json.dumps(index))

    tar.extractall(gimp_plugins_dir, members=files)


def uninstall(plugin_name):
    with open(gpi_config_file, 'r') as f:
        index = json.load(f)
        if plugin_name not in index:
            return False

    directories = []
    for file in index[plugin_name]['files']:
        # TODO remove empty directories
        full_path = os.path.join(gimp_plugins_dir, file)
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
    """Return human readable info about an installed package"""
    info = 'Name: {}\n'.format(plugin_name)
    if 'description' in plugin_metadata:
        info += 'Description: {}\n'.format(plugin_metadata['description'])
    info += 'Version: {}\n'.format(plugin_metadata['version'])
    info += 'Installed: True\n'
    return info

def remote_info(plugin_name):
    """Return human readable info about a package which is not installed.
    Fetches info from the server."""
    try:
        plugin_info = get_package_info(plugin_name)
    except PackageNotFound:
        return ('Sorry, a package named' +
            '{} couldn\'t be found :( \n').format(plugin_name)
    available_versions = map(
        lambda release: release['version'],
        plugin_info['releases']
    )
    pretty_available_versions = reduce(
        lambda available, version: available + ', ' + version,
        available_versions
    )
    info = 'Name: {}\n'.format(plugin_name)
    if 'description' in plugin_metadata:
        info += 'Description: {}\n'.format(plugin_metadata['description'])
    info += 'Available versions: {}\n'.format(pretty_available_versions)
    info += 'Installed: False\n'
    return info


def list_installed():
    """Returns a list of all installed packages registered with gpi"""
    if os.path.isfile(gpi_config_file):
        with open(gpi_config_file, 'r') as f:
            index = json.load(f)
        installed = ''
        for plugin in index:
            version = index[plugin]['version']
            installed +='{}=={}\n'.format(plugin, version)
        return installed
    else:
        return ''
