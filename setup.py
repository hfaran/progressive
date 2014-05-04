import os
import sys
import codecs

from setuptools import setup
from setuptools.command.test import test as TestCommand

import progressive


here = os.path.abspath(os.path.dirname(__file__))
def read(filename):
    """Read and return `filename` in root dir of project and return string"""
    return codecs.open(os.path.join(here, filename), 'r').read()


install_requires = read("requirements.txt").split()
long_description = read('README.rst')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--verbose']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name="progressive",
    version=progressive.__version__,
    url='https://github.com/hfaran/progressive',
    license='MIT License',
    author='Hamza Faran',
    description=('Terminal progress bars for Python with blessings'),
    long_description=long_description,
    packages=['progressive'],
    install_requires = install_requires,
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    extras_require={
        'testing': ['pytest'],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Environment :: Console',
        'Environment :: Console :: Curses',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        'Operating System :: POSIX',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Terminals',
    ]
)
