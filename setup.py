from distutils.core import setup
from setuptools import find_packages

setup(
    name='gpi',
    version='0.1.1',
    author=u'Evan Tschuy',
    author_email='evantschuy@gmail.com',
    packages=find_packages(),
    url='https://gpi.tschuy.com',
    license='',
    scripts=['bin/gpi'],
    description="The GIMP Plugin Installer command-line tool",
    long_description=open('README.md').read()
)
