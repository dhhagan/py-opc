#!/usr/bin/env python3

__version__ = '0.2.0'

from distutils.core import setup

setup(
    name = 'opc',
    version = __version__,
    packages = ['opc'],
    description = 'Python libary for operating the Alphasense OPC-N2',
    author = 'David H Hagan',
    author_email = 'david@davidhhagan.com',
    license = 'MIT',
    url = 'https://github.com/dhhagan/py-opc',
    keywords = ['opc', 'alphasense', 'atmospheric chemistry'],
    classifiers = [
        'Development Status :: 1 - alpha',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: System :: Hardware',
        'Topic :: System :: Hardware Drivers',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
