# pylint: disable=W0201, C0415
"""
Flask RESTful Quick Start Setup
"""

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

NAME = 'flask-quickstart'
VERSION = '0.2'
AUTHOR = 'Keath Milligan'
REQUIRED_PYTHON_VERSION = (3, 8)
PACKAGES = ['sample']
INSTALL_DEPENDENCIES = [
    'Flask',
    'Flask-SQLAlchemy',
    'Flask-Marshmallow',
    'Marshmallow-SQLAlchemy',
    'flask-jwt-extended'
]
SETUP_DEPENDENCIES = [
]
TEST_DEPENDENCIES = [
    'pytest'
]
EXTRA_DEPENDENCIES = {
    'dev': [
        'pytest',
        'pylint',
        'pylint-flask',
        'pylint-flask-sqlalchemy'
    ],
    'doc': [
        'Sphinx'
    ]
}

if sys.version_info < REQUIRED_PYTHON_VERSION:
    sys.exit(f'Python >= {REQUIRED_PYTHON_VERSION[0]}.{REQUIRED_PYTHON_VERSION[1]}'
             ' is required. Your version: {sys.version}')


class PyTest(TestCommand):
    """
    Use pytest to run tests
    """
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    packages=PACKAGES,
    include_package_data=True,
    install_requires=INSTALL_DEPENDENCIES,
    setup_requires=SETUP_DEPENDENCIES,
    tests_require=TEST_DEPENDENCIES,
    extras_require=EXTRA_DEPENDENCIES,
    cmdclass={
        'test': PyTest
    }
)
