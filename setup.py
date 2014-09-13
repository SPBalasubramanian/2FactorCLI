#!/usr/bin/env python
# coding=utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pip.req import parse_requirements

config = {
    'name': '2factorcli',
    'version': '1.1.3',
    'description': 'This is a simple python program to allow you to store and '
    ' generate time-based one-time passwords in a GPG encrypted vault.',
    'author': 'Rob Smith',
    'author_email': 'kormoc@gmail.com',
    'url': 'https://github.com/kormoc/2FactorCLI',
    'scripts': ['2factorcli'],
    'license': 'MIT',
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
}

with open('README.md', 'r') as fp:
    config['long_description'] = fp.read()

install_reqs = parse_requirements('requirements.txt')
config['install_requires'] = [str(ir.req) for ir in install_reqs]

setup(**config)
