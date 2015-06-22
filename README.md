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
    "url": "https://github.com/tschuy/gimp-export-to-imgur",
    "description": "Upload your images to Imgur directly from the Save menu"
}
```
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

1. Remove empty folders on uninstall
2. Catch duplicate files and disallow uninstallation (or fix GIMP to allow recursive plugin finding)
3. Install plugins from git
4. Documentation
5. Code cleanup
6. Allow the use of a virtualenv to install packages from pip
7. Add verbose mode
