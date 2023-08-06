#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, division, print_function

import os
import re
import sys

from setuptools import setup

readme = open('README.rst').read()

setup(
    name='django-tabular-export',
    version='1.1.0',
    description="""Simple spreadsheet exports from Django""",
    long_description=readme,
    author='Chris Adams',
    author_email='cadams@loc.gov',
    url='https://github.com/LibraryOfCongress/django-tabular-export',
    packages=[
        'tabular_export',
    ],
    include_package_data=True,
    install_requires=[
        'Django',
        'xlsxwriter',
    ],
    test_suite='tests.run_tests.run_tests',
    license='CC0',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
