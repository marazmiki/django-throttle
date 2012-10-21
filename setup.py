#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import sys
import datetime

ROOT_PACKAGE = 'django-throttle'
VERSION = '0.2'

def long_description():
    """
    Returns package long description from README.rst
    """
    def read(what):
        return open(os.path.join(
                    os.path.dirname(__file__), '{0}.md'.format(what))).\
                    read()


    return "{README}\n\n{CHANGELOG}".format(README=read('README'),
                                            CHANGELOG=read('CHANGELOG'))

def version():
    """
    Returns package version for package building
    """
    return VERSION


if __name__ == '__main__':
    setup(name=ROOT_PACKAGE,
          description='Simple application for throttling HTTP requests to views',
          author='marazmiki',
          author_email='marazmiki@gmail.com',
          version=version(),
          long_description=long_description(),
          packages=find_packages(),
          classifiers  = [
              'Environment :: Web Environment',
              'Programming Language :: Python',
              'Framework :: Django'
          ],
    )
