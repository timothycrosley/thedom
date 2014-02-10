#!/usr/bin/env python

import subprocess
import sys

try:
    from setuptools import setup
    from setuptools.command.test import test as TestCommand

    class PyTest(TestCommand):
        extra_kwargs = {'tests_require': ['pytest', 'mock']}

        def finalize_options(self):
            TestCommand.finalize_options(self)
            self.test_args = []
            self.test_suite = True

        def run_tests(self):
            import pytest
            sys.exit(pytest.main(self.test_args))

except ImportError:
    from distutils.core import setup, Command

    class PyTest(Command):
        extra_kwargs = {}
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            raise SystemExit(subprocess.call([sys.executable, 'runtests.py']))

try:
   import pypandoc
   readme = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError, OSError, RuntimeError):
   readme = ''

setup(name='thedom',
      version='0.0.1',
      long_description=readme,
      description='thedom is a collection of python objects that enable you to represent and interact with the DOM server side before generating HTML, CSS, and JavaScript for the client.',
      author_email='timothy.crosley@gmail.com',
      url='https://github.com/timothycrosley/webelements',
      download_url='https://github.com/timothycrosley/webelements/archive/1.0.0-beta.2.tar.gz',
      license="MIT",
      packages=['thedom'],
      requires=['pies'],
      install_requires=['pies>=2.5.5'],
      cmdclass={'test': PyTest},
      keywords='Web, Python, Python2, Python3, Dom, HTML, Library, Parser',
      classifiers=['Development Status :: 6 - Mature',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.0',
                   'Programming Language :: Python :: 3.1',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Software Development :: Libraries'],
      **PyTest.extra_kwargs)
