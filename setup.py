'''
File: setup.py
Description: Bolt server installation script
Author: Saurabh Badhwar <sbadhwar@redhat.com>
Date: 27/09/2017
'''
from setuptools import setup, find_packages
setup(
    name='bolt_server',
    version='1.0.0_beta',
    packages=find_packages(exclude=['docs', 'tests', 'temp'])
)
