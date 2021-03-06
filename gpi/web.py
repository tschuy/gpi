import io
import os
import urllib2
import json
import tarfile

host = os.environ.get('GPI_HOST', "https://gpi.tschuy.com")


class PackageNotFound(Exception):
    """
    The exception thrown if the package 404s
    """


class PackageReadError(Exception):
    """
    The exception thrown if the package cannot be read
    """
    def __init__(self, url):
        super(PackageReadError, self).__init__(url)


def get_packages():
    """Retrieves a list of available packages from the GPI host"""
    url = "{}/api/packages".format(host)
    response = urllib2.urlopen(url)

    packages = json.loads(response.read())
    return packages


def get_package_info(package_name):
    """Retrieve the package metadata as json from the GPI host"""
    url = "{}/api/package/{}".format(host, package_name)
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError:
        raise PackageNotFound

    package_info = json.loads(response.read())
    return package_info


def get_from_web(package_name, package_url=None):
    if not package_url:
        package_info = get_package_info(package_name)
        package_url = "{}{}".format(
            host, package_info['releases'][0]['file'])
    file = urllib2.urlopen(package_url).read()

    try:
        return tarfile.open(fileobj=io.BytesIO(file), mode='r')
    except:
        raise PackageReadError(package_url)
