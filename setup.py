#!/usr/bin/python
# -*-coding:utf-8-*-

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'cnprep',
    version = '0.1.12',
    description = 'A lib for Chinese text preprocessing',
    author = 'Keming Yang',
    author_email = 'a398445075@gmail.com',
    url = 'https://github.com/momingcoder/cnprep',
    download_url = 'https://github.com/momingcoder/cnprep/tarball/0.1.12',
    license = 'MIT',
    keywords = ['Chinese', 'text', 'preprocess'],
    classifiers = [
        'Topic :: Text Processing',
        'Programming Language :: Python :: 3.5',
    ],
    packages = find_packages(),
    install_requires = ['xpinyin'],
    platform = ['Windows', 'Linux', 'Mac'],
    long_description=long_description,
)
