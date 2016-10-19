'''
    py-opc is a python library to operate the Alphasense
    OPC-N2 optical particle counter.

    Written originally by David H Hagan
'''

__version__ = '1.3.0'

try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name = 'py-opc',
    version = __version__,
    packages = ['opc'],
    description = 'Python libary for operating the Alphasense OPC-N2 optical particle counter',
    author = 'David H Hagan',
    author_email = 'david@davidhhagan.com',
    license = 'MIT',
    url = 'https://github.com/dhhagan/py-opc',
    keywords = ['opc', 'alphasense', 'atmospheric chemistry'],
    test_suite = 'tests',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Topic :: Scientific/Engineering :: Atmospheric Science',
		'Topic :: Software Development',
        'Topic :: System :: Hardware',
    ]
)
