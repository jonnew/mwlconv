#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setupi, find_packages
from codecs import open
from os import path

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup (
    name = 'mwlconv',
    description = 'File conversion tools for MWL.',
    version = '1.0.0',
    install_requires = ['nose'],
    packages=find_packages(),
    scripts = [],
    license = 'GPL-3.0',
    long_description = long_description,
    include_package_data=True,
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    entry_points={
        'console_scripts': [
            'oat2x = oat2x:main',
        ],
    }
)
