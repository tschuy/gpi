import os
import json

gimp_plugins_dir = os.environ.get(
    'GIMP_PLUGIN_DIR', os.path.expanduser("~/.gimp-2.8/plug-ins/"))

gpi_config_file = gimp_plugins_dir + '.gpi.json'

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
        if os.path.isdir(gimp_plugins_dir + file):
            directories.append(gimp_plugins_dir + file)
        else:
            os.remove(gimp_plugins_dir + file)

    del index[plugin_name]
    with open(gpi_config_file, 'w') as f:
        f.write(json.dumps(index))

    return True
