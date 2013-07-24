from setuptools import setup, find_packages
import sys, os

version = '0.0'

requires = [
    'trumpet>=0.1.1dev', # pull from github
    ]


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
      install_requires=requires,
      dependency_links=[
        'https://github.com/umeboshi2/trumpet/archive/master.tar.gz#egg=trumpet-0.1.1dev',
        'https://github.com/umeboshi2/hubby/archive/master.tar.gz#egg=hubby-0.0dev',
        ],
      entry_points="""
      # -*- Entry points: -*-
      [paste.app_factory]
      main = mslemon:main
      [fanstatic.libraries]
      mslemon_lib = mslemon.resources:library
      mslemon_css = mslemon.resources:css
      mslemon_js = mslemon.resources:js
      """,
      )
