# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from setuptools import find_packages, setup

try:
    long_description = open('README.rst').read()
except IOError:
    long_description = open('README.md').read()


version = '1.1'

setup(
    name='geopip',
    version=version,
    packages=find_packages(),
    install_requires=[
        'geohash-hilbert',
        # 'numpy',
        # 'shapely[vectorized]>=1.6b4',
    ],
    author='Tammo Ippen',
    author_email='tammo.ippen@posteo.de',
    description='Reverse geocode a lng/lat coordinate within a geojson FeatureCollection.',
    long_description=long_description,
    url='https://github.com/tammoippen/geopip',
    license='MIT',
    download_url='https://github.com/tammoippen/geopip/archive/v{}.tar.gz'.format(version),
    keywords=['geojson', 'point in polygon', 'reverse geocode', 'countries'],
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
