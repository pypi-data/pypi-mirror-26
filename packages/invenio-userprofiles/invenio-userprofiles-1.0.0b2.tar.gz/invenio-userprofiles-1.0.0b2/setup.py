# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016, 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""User profiles module for Invenio."""

import os
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'SQLAlchemy-Continuum>=1.2.1',
    'check-manifest>=0.25',
    'coverage>=4.0',
    'invenio-i18n>=1.0.0b2',
    'isort>=4.2.2',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
]

extras_require = {
    'admin': [
        'invenio-admin>=1.0.0b1',
    ],
    'docs': [
        'Sphinx>=1.4.2',
        'invenio-mail>=1.0.0b1',
    ],
    'mysql': [
        'invenio-db[mysql]>=1.0.0b3',
    ],
    'postgresql': [
        'invenio-db[postgresql]>=1.0.0b3',
    ],
    'sqlite': [
        'invenio-db>=1.0.0b3',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name in ('mysql', 'postgresql', 'sqlite'):
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'pytest-runner>=2.6.2',
    'Babel>=1.3',
]

install_requires = [
    'Flask-BabelEx>=0.9.3',
    'Flask-Breadcrumbs>=0.3.0',
    'Flask-Mail>=0.9.1',
    'Flask-Menu>=0.4.0',
    'Flask-WTF>=0.13.1',
    'Flask>=0.11.1',
    'invenio-accounts>=1.0.0b3',
    'WTForms>=2.0.1',
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_userprofiles', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-userprofiles',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio profile account user',
    license='GPLv2',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-userprofiles',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_admin.views': [
            'invenio_userprofiles_view = '
            'invenio_userprofiles.admin:user_profile_adminview',
        ],
        'invenio_base.api_apps': [
            'invenio_userprofiles = invenio_userprofiles:InvenioUserProfiles',
        ],
        'invenio_base.api_blueprints': [
            'invenio_userprofiles'
            ' = invenio_userprofiles.views:blueprint_api_init',
        ],
        'invenio_base.apps': [
            'invenio_userprofiles = invenio_userprofiles:InvenioUserProfiles',
        ],
        'invenio_base.blueprints': [
            'invenio_userprofiles'
            ' = invenio_userprofiles.views:blueprint_ui_init',
        ],
        'invenio_db.alembic': [
            'invenio_userprofiles = invenio_userprofiles:alembic',
        ],
        'invenio_db.models': [
            'invenio_userprofiles = invenio_userprofiles.models',
        ],
        'invenio_i18n.translations': [
            'messages = invenio_userprofiles',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 4 - Beta',
    ],
)
