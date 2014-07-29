#!/usr/bin/env python3
# coding=utf-8

from distutils.core import setup
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='2factorcli',
    version='0.0.1',
    description='This is a simple python program to allow you to store and generate time-based one-time passwords in a GPG encrypted vault.',
    long_description=open('README.md').read(),
    author='Rob Smith',
    author_email='kormoc@gmail.com',
    url='https://github.com/kormoc/2FactorCLI',
    packages=[],
    scripts=['2factorcli.py'],
    license='MIT',
    install_requires=reqs,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
