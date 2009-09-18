# -*- coding: utf-8 -*-
"""
This module contains the tool of hc.recipe.django
"""

import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

MAJOR = 0
MINOR = 1
PATCH = 0

name = 'hc.recipe.download'
version = '%s.%s.%s' % (MAJOR, MINOR, PATCH)
long_description = '\n'.join([
    read('docs', 'README.txt'),
    'Changelog',
    '*********',
    '',
    read('docs', 'CHANGES.txt'),
    'Detailed Documentation',
    '**********************',
    '',
    read('hc', 'recipe', 'download', 'README.txt'),
])
tests_require = ['zope.testing']


setup( 
    name=name,
    version=version,
    description="A buildout recipe for downloading files and packages",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
    ],
    keywords='buildout recipe',
    author='Jacob Radford',
    author_email='webmaster@hunter.cuny.edu',
    url='http://github.com/hcwebdev/hc.recipe.download/',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['hc', 'hc.recipe'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zc.buildout',
        # -*- Extra requirements: -*-
    ],
    tests_require=tests_require,
    extras_require=dict(tests=tests_require),
    test_suite = '%s.tests.test_suite' % name,
    entry_points= {
        'zc.buildout': ['default = %s:Recipe' % name]
    },
)
