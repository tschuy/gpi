import io
import os
import urllib2
import json
import tarfile

host = os.environ.get('GPI_HOST', "http://gpi.tschuy.com")


class PackageNotFound(Exception):
    """
    The exception thrown if the package 404s
    """


class PackageReadError(Exception):
    def __init__(self, url):
        super(PackageReadError, self).__init__(url)
    """
    The exception thrown if the package cannot be read
    """


def get_from_web(package_name):
    url = "{}/api/package/{}".format(host, package_name)
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError:
        raise PackageNotFound

    package_info = json.loads(response.read())
    url = "{}{}".format(
        host, package_info['releases'][0]['file'])
    file = urllib2.urlopen(url).read()

    try:
        return tarfile.open(fileobj=io.BytesIO(file), mode='r')
    except:
        raise PackageReadError(url)
