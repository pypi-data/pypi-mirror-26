#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages
import nagiosunity


def read_requires(filename):
    with open(filename, "r") as f:
        return f.read().splitlines()


def read_raw(filename):
    with open(filename, "r") as f:
        return f.read()


setup(
    name='nagios-unity',
    version=nagiosunity.__version__,
    description=(
        'Unity plugin for Nagios.'
    ),
    long_description=read_raw('README.rst'),
    author='Peter Wang',
    author_email='peter.wang13@dell.com',
    maintainer='Peter Wang',
    maintainer_email='peter.wang13@dell.com',
    license='Apache Software License',
    packages=find_packages(),
    platforms=["all"],
    url='http://github.com/thecodeteam/nagios-unity',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],

    install_requires=read_requires('requirements.txt'),
    tests_require=read_requires('test-requirements.txt'),
    entry_points={
        'console_scripts': [
            'nagios-unity=nagiosunity.cli.client:main',
        ],
    },
)
