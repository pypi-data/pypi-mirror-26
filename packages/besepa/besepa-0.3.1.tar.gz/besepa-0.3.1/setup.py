#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

from besepa.config import __version__

long_description = """
    The Besepa Python provides simple python wrapper to Besepa.com's API.

    1. https://github.com/txerpa/besepa-python - README and Samples
    2. http://docs.besepaen.apiary.io - API Reference
"""

setup(
  name='besepa',
  version=__version__,
  author='Mateu Cànaves',
  author_email='mateu.canaves@gmail.com',
  packages=['besepa'],
  scripts=[],
  url='https://github.com/txerpa/besepa-python',
  license='MIT',
  description="Simple python wrapper to Besepa.com's API.",
  long_description=long_description,
  install_requires=['requests'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules'
  ],
  keywords=['besepa', 'rest', 'sdk', 'debits', 'sepa']
)
