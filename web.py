import os

host = os.environ.get('GPI_HOST', "http://localhost:8000/")

def get_from_web(package_name, host):
    response = urllib2.urlopen(host + args.command[1] + '.tar.gz')
    print response.read()
