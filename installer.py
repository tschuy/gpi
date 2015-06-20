import os
import json

gimp_plugins_dir = os.environ.get(
    'GIMP_PLUGIN_DIR', os.path.expanduser("~/.gimp-2.8/plug-ins/"))


def plugin_config_file(plugin_name):
    return gimp_plugins_dir + '.' + plugin_name


def install(tar, manifest):
    with open(plugin_config_file(manifest['identifier']), 'w') as f:
        files = [t for t in tar if t.name != 'gpi.json']
        plugin_info = {
            'version': manifest['version'],
            'name': manifest['name'],
            'files': [file.name for file in files]
        }
        f.write(json.dumps(plugin_info))

    tar.extractall(gimp_plugins_dir, members=files)


def uninstall(config):
    with open(config, 'r') as f:
        data = json.load(f)

        directories = []
        for file in data['files']:
            if os.path.isdir(gimp_plugins_dir + file):
                directories.append(gimp_plugins_dir + file)
            else:
                os.remove(gimp_plugins_dir + file)

        # TODO remove empty directories
        os.remove(config)
