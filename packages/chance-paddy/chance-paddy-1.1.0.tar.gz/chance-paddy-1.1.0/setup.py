#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: setup.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 19.10.2017
from setuptools import setup

from paddy import __version__


setup(
    name='chance-paddy',
    version=__version__,
    description='The base trader for chancefocus',
    url='https://gitee.com/QianFuFinancial/paddy.git',
    author='Jimin Huang',
    author_email='huangjimin@whu.edu.cn',
    license='MIT',
    packages=['paddy'],
    install_requires=[
        'nose>=1.3.7',
        'coverage>=4.1',
        'requests>=2.13.0',
    ],
    zip_safe=False,
)
