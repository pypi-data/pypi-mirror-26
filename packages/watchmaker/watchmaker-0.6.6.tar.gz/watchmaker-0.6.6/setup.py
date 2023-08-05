#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Watchmaker setup script."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import io
import os
import re
import sys

from setuptools import find_packages, setup


def read(*names, **kwargs):
    """Read a file."""
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


def find_version(*file_paths):
    """Read the version number from a source file."""
    # Why read it, and not import?
    # see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion
    version_file = read(*file_paths, encoding='utf8')

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def parse_md_to_rst(files):
    """Read Markdown files and convert them to ReStructured Text."""
    rst = []
    try:
        from m2r import parse_from_file
        for name in files:
            rst += [parse_from_file(name)]
    except ImportError:
        # m2r may not be installed in user environment
        for name in files:
            rst += [read(name)]
    return '\n'.join(rst)


install_requires = [
    "click",
    "futures",
    "six",
    "PyYAML",
]

if sys.version_info[0:2] <= (2, 6):
    install_requires += ["wheel<=0.29.0"]

setup(
    name='watchmaker',
    version=find_version('src', 'watchmaker', '__init__.py'),
    license='Apache Software License 2.0',
    author='Plus3IT Maintainers of Watchmaker',
    author_email='projects@plus3it.com',
    description='Applied Configuration Management',
    long_description=parse_md_to_rst(['README.md', 'CHANGELOG.md']),
    url='https://github.com/plus3it/watchmaker',
    packages=find_packages(str('src')),
    package_dir={'': str('src')},
    include_package_data=True,
    platforms=[
        'Windows',
        'Linux'
    ],
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'watchmaker = watchmaker.cli:main',
            'wam = watchmaker.cli:main',
        ]
    },
    install_requires=install_requires
)
