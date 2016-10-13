#!/usr/bin/env python

from setuptools import setup
from ipwb import __version__

long_description = open('README.rst').read()

setup(
    name='ipwb',
    version=__version__,
    url='https://github.com/oduwsdl/ipwb',
    download_url="https://github.com/oduwsdl/ipwb",
    author='Mat Kelly',
    author_email='mkelly@cs.odu.edu',
    description="""InterPlanetary Wayback (ipwb):
      Web Archive integration with IPFS""",
    packages=['ipwb'],
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
    entry_points="""
        [console_scripts]
        ipwb = ipwb.__main__:main
    """,
    keywords='http web archives ipfs distributed odu wayback',
    classifiers=[
      'Development Status :: 2 - Pre-Alpha',

      'Environment :: Web Environment',

      'Programming Language :: Python :: 2.7',

      'License :: OSI Approved :: MIT License',

      'Intended Audience :: Developers',
      'Intended Audience :: Information Technology',
      'Intended Audience :: Science/Research',

      'Topic :: Internet :: WWW/HTTP',
      'Topic :: System :: Archiving',
      'Topic :: System :: Archiving :: Backup',
      'Topic :: System :: Archiving :: Mirroring',
      'Topic :: Utilities',
    ]
)
