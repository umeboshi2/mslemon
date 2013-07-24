from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='mslemon',
      version=version,
      description="Miss Lemon",
      long_description="""\
PhoneSlips and NoteTaking""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Joseph Rawson',
      author_email='joseph.rawson.works@littledebian.org',
      url='',
      license='Public Domain',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
