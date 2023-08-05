from setuptools import setup, find_packages
import unittest

install_requires = []

with open("README.md") as f:
    long_description = f.read()

def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

setup(name='anyloadump',
      version='0.1',
      description='dumper and loader for various file formats.',
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
      ],
      packages=find_packages(exclude=["tests"]),
      url="https://github.com/knknkn1162/anyloadump",
      author="knknkn1162",
      author_email="knknkn1162@gmail.com",
      include_package_data=True,
      zip_safe=False,
      test_suite="setup.my_test_suite",
      license="MIT",
      keywords="",
      install_requires=install_requires,
      entry_points="""
""")
