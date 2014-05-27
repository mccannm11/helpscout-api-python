#!/usr/bin/python

from __future__ import print_function
from setuptools import setup, find_packages

setup(name='helpscout',
      version='0.0.1',
      description='Helpscout API Wrapper',
      author='Mike McCann',
      author_email='michael@mccanns.org',
      packages=['helpscout'],
      package_dir={'soundcloud': 'soundcloud'},
      install_requires=['requests>=0.14.0']
      )