# -*- coding: utf 8 -*-
"""
Python installation file for jeepr project.
"""
from setuptools import setup
import re

verstr = 'unknown'
VERSIONFILE = "jeepr/_version.py"
with open(VERSIONFILE, "r")as f:
    verstrline = f.read().strip()
    pattern = re.compile(r"__version__ = ['\"](.*)['\"]")
    mo = pattern.search(verstrline)
if mo:
    verstr = mo.group(1)
    print("Version "+verstr)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

REQUIREMENTS = ['numpy',
                'matplotlib',
                'scipy',
                'tqdm',
                'beautifulsoup4',
                'h5py',
                ]

TEST_REQUIREMENTS = ['pytest',
                     'coveralls',
                     'pytest-cov',
                     'pytest-mpl',
                     ]

# Test command is:
# py.test --mpl --cov striplog

CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'Intended Audience :: Science/Research',
               'Natural Language :: English',
               'License :: OSI Approved :: Apache Software License',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6',
               ]

setup(name='jeepr',
      version=verstr,
      description='Tools for managing GPR data.',
      url='http://github.com/agile-geoscience/jeepr',
      author='Agile Scientific',
      author_email='hello@agilescientific.com',
      license='Apache 2',
      packages=['jeepr'],
      tests_require=TEST_REQUIREMENTS,
      test_suite='run_tests',
      install_requires=REQUIREMENTS,
      classifiers=CLASSIFIERS,
      zip_safe=False,
      )
