#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: setup
   :synopsis: Setup script to use with pip for the project pyXraySpectrumFileFormat.

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Setup script to use with pip for the project pyXraySpectrumFileFormat.
"""

###############################################################################
# Copyright 2015 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Standard library modules.
import os.path

# Third party modules.
from setuptools import setup, find_packages

# Local modules.

# Globals and constants variables.
with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'numpy',
    'matplotlib',
    'scipy',
    'six'
]

test_requirements = [
    'nose', 'coverage'
]

readme_file_path = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(readme_file_path).read() + '\n\n'

setup(name="pySpectrumFileFormat",
    version='0.1',
    url='',
    description="Project to read and write various x-ray spectrum file format.",
	long_description=readme + '\n\n' + history,
	author="Hendrix Demers",
	author_email="hendrix.demers@mail.mcgill.ca",
	license="Apache License, Version 2.0",
	classifiers=['Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
		'Natural Language :: English',
		'Programming Language :: Python',
		'Operating System :: OS Independent',
		'Topic :: Scientific/Engineering',],

    packages=find_packages(),
#    package_dir={'microanalysis_file_format':
#                 'microanalysis_file_format'},
    install_requires=requirements,
    zip_safe=False,
    keywords='microanalysis_file_format',

	include_package_data=False, # Do not include test data

    setup_requires=['nose', 'coverage'],

    test_suite='nose.collector',
    tests_require=test_requirements

)

