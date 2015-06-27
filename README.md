# GIMP Plugin Installer

[![Build Status](https://travis-ci.org/tschuy/gpi.svg)](https://travis-ci.org/tschuy/gpi)

Install GIMP plugins from the command line with a simple, easy to use package
manager.

Usage
-----

Install from gpi-web:

```
$ gpi install imguruploader
```

Uninstall an installed package:
```
$ gpi uninstall imguruploader
```

Install from a locally downloaded file:
```
$ gpi install -f ~/imgur-uploader.tar.gz
```

Anatomy of a gpi package (aka how to package your plugin)
---------------------------------------------------------

The root level of a gpi package requires two things: a ``gpi.json`` manifest
file, and a ``contents/`` directory. The ``contents/`` directory will be
extracted directly to the user's GIMP plugin directory, so make sure you only
include files necessary for your plugin. You can put other content, like a
LICENSE or CHANGELOG, in the root of the package. Files outside of ``contents/``
will be ignored.

Your ``gpi.json`` file should look like this:

```
{
    "version": "0.1.0",
    "name": "Imgur Uploader",
    "identifier": "imguruploader",
    "author": "tschuy",
    "license": "MIT",
    "type": "python",
    "url": "https://github.com/tschuy/gimp-export-to-imgur",
    "description": "Upload your images to Imgur directly from the Save menu"
}
```

The type of a plugin can either by ``python`` or ``scriptfu``. If it is missing,
``gpi`` will assume the plugin is Python and extract it to the ``plug-ins``
directory.

To test your plugin, pass your ``.tar.gz`` to gpi with the ``-f`` flag. Open
GIMP, and verify your plugin works as expected.

Testing gpi
-----------

Currently, ``gpi`` has very limited tests. Pull requests with additional tests
are happily accepted!

``gpi`` uses Python's built-in ``unittest`` library. To run the tests, run
``python setup.py test`` within the root of the repository.

A pre-commit hook has been provided for your convenience. This hook runs the
test suite (which takes approximately two seconds) and the PEP8 flaker. (For
the flaker to work, install ``flake8`` with pip.) To use this hook, copy
``tests/pre-commit`` into ``.git/hooks/``.

Issues
------

0. GIMP plugin for installing plugins!
1. Remove empty folders on uninstall
2. Catch duplicate files and disallow uninstallation (or fix GIMP to allow recursive plugin finding)
3. Install plugins from git
4. Documentation
5. Code cleanup
6. Allow the use of a virtualenv to install packages from pip
7. Add verbose mode

Architecture
------------

``gpi``'s backend is laid out into two different install modules, with a
separate executable for the command line program and, soon, a fourth file for
mangaging plugins directly from GIMP itself.

Anything web-related goes in ``gpi.web``. These functions interface with the
web portion of GPI, so the ``get_from_web`` function that returns a ``tarfile``
object for a given package name lives in here, as does the function to get
package info from the API.

``gpi.web`` is currently in need of tests.

In ``gpi.installer`` lives the generic installer/uninstaller functions. Here you
can install a plugin with ``gpi.installler.install``, uninstall with
``gpi.installler.uninstall``. This module also holds some generic information
like the ``info`` commands for getting local/remote package info, as well as
the plugin list. These should be moved to more appropriate modules in the
future.

``gpi.installer`` is currently well-tested.

Lastly, the command line executable lives in ``bin/gpi``. This executable is
home to the args parsing, and decides which code paths to take.

``bin/gpi`` needs tests, and should be re-written.
