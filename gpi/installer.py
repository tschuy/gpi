import json
import os
import sys

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
