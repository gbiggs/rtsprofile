#!/usr/bin/env python
# -*- Python -*-
# -*- coding: utf-8 -*-

'''rtsprofile

Copyright (C) 2009-2015
    Geoffrey Biggs
    RT-Synthesis Research Group
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the GNU Lesser General Public License version 3.
http://www.gnu.org/licenses/lgpl-3.0.en.html

File: setup.py

Install script.

'''

__version__ = '$Revision: $'
# $Source$


from distutils.core import setup
import sys


setup(name='rtsprofile',
      version='4.0.0',
      description='Library to read, manipulate and write RT system profiles \
using the RTSProfile XML schema.',
      long_description='Library to read, manipulate and write RT system \
profiles using the RTSProfile XML schema.',
      author='Geoffrey Biggs',
      author_email='git@killbots.net',
      url='http://github.com/gbiggs/rtsprofile',
      license='LGPL3',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development',
          ],
      packages=['rtsprofile']
      )


# vim: tw=79

