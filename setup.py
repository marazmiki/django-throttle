#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import os


ROOT_PACKAGE = 'django-throttle'
VERSION = '0.3'


def long_description():
    """
    Returns package long description from README.rst
    """
    def read(what):
        filename = os.path.join(
            os.path.dirname(__file__),
            '{0}.rst'.format(what))
        with open(filename) as fp:
            return fp.read()

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
          test_suite='tests.main',
          classifiers=[
              'Environment :: Web Environment',
              'Programming Language :: Python',
              'Framework :: Django'
          ])
