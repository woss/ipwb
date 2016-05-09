#!/usr/bin/env python

from setuptools import setup, find_packages
from ipwb import __version__

long_description = open('README.md').read()

setup(
    name='ipwb',
    version=__version__,
    url='https://github.com/oduwsdl/ipwb',
    author='Mat Kelly',
    author_email='mkelly@cs.odu.edu',
    description='Web Archive integration with IPFS',
    packages=['ipwb',],
    license='MIT',
    long_description=long_description,
    provides=[
      'ipwb'
    ],
    install_requires=[
      'pywb',
      'surt',
      'ipfs-api'
    ],
    classifiers=[
    
    ]
)