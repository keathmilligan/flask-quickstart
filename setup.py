"""
Flask RESTful Quick Start Setup
"""

import sys
import os
from setuptools import setup
from setuptools.command.test import test as TestCommand
from setuptools.command.develop import develop as DevelopCommand

# check python version
if sys.version_info < (3,3):
    sys.exit('Python >= 3.3 is required. Your version:\n'+sys.version)


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


# installation dependencies
install_dependencies = [
    'Flask',
    'Flask-SQLAlchemy',
    'Flask-Marshmallow',
    'Marshmallow-SQLAlchemy',
    'Flask-JWT'
]

# setup dependencies
setup_dependencies = []

# test dependencies
test_dependencies = [
    'pytest'
]

setup(
    name='flask-quickstart',
    version='0.1',
    packages=['sample'],
    include_package_data=True,
    install_requires=install_dependencies,
    setup_requires=setup_dependencies,
    tests_require=test_dependencies,
    cmdclass={'test': PyTest}
)
