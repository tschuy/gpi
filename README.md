# GIMP Plugin Installer

![Build Status](https://travis-ci.org/tschuy/gpi.svg)

Install GIMP plugins from the command line with a simple, easy to use package
manager.

Usage
-----

``gpi install imguruploader``
``gpi uninstall imguruploader``
``gpi install -f ~/imgur-uploader.tar.gz``


ToDo:

1. Django app to fetch plugins from
2. Remove empty folders!
3. Standardize ``gpi.json``
4. Catch duplicate files
5. Install from file
6. Install from git
7. Documentation
8. Code cleanup
9. TESTS
10. Allow usage of pip-installed packages?

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
    "name": "ImgurUploader",
    "identifier": "imguruploader"
}
```

Now, you can pass this file to ``gpi`` and it will install your plugin.
