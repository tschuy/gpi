# GIMP Plugin Installer

![Build Status](https://travis-ci.org/tschuy/gpi.svg)

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

How to package your plugin
--------------------------

To package your plugin, place any required files into a tar.gz file. This
tarfile will be extracted directly into your user's plugins folder, and so be
sure to only include necessary files. If you want extra files, consider making
a directory named after your plugin and putting them in there.

Then, add a ``gpi.json`` file to your tarfile. It should look like this:

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

Now, you can pass this file to ``gpi`` and it will install your plugin.

Testing
-------

Currently, ``gpi`` has no tests. This is a major issue and will be rectified as
soon as possible.

Issues
------

1. Remove empty folders on uninstall
2. Catch duplicate files and disallow uninstallation (or fix GIMP to allow recursive plugin finding)
3. Install plugins from git
4. Documentation
5. Code cleanup
6. Allow the use of a virtualenv to install packages from pip
