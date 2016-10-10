#!/usr/bin/python
# -*-coding:utf-8-*-

# from distutils.core import setup
from setuptools import setup, find_packages

setup(
  name = 'cnprep',
  version = '0.1.10',
  description = 'A lib for Chinese text preprocessing',
  author = 'MomingCoder',
  author_email = 'a398445075@gmail.com',
  url = 'https://github.com/momingcoder/cnprep', # use the URL to the github repo
  download_url = 'https://github.com/momingcoder/cnprep/tarball/0.1.10',
  license = 'MIT',
  keywords = ['Chinese', 'text', 'preprocess'], # arbitrary keywords
  classifiers = ['Topic :: Text Processing'],
  packages = find_packages(),
  install_requires = ['xpinyin'],
  platform = ['Windows', 'Linux', 'Mac'],
)
