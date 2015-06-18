# GIMP Plugin Installer

```
tschuy@tschuy-laptop:(gpi)(master) → gpi install imguruploader
ImgurUploader 0.1.0 installed successfully!
tschuy@tschuy-laptop:(gpi)(master) → gpi uninstall imguruploader
ImgurUploader 0.1.0 uninstalled successfully!
tschuy@tschuy-laptop:(gpi)(master) →
```

Install GIMP plugins from the command line with a simple, easy to use package
manager.

Future:

1. Django app to fetch plugins from
2. Remove empty folders!
3. Standardize ``gpi.json``
4. Catch duplicate files
5. Install from file
6. Install from git

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
