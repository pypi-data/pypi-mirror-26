#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='rws',
      version='0.6',
      description='Ranking Web Server',
      author='Algorithm Ninja',
      license='AGPL3',
      url='https://github.com/algorithm-ninja/rws',
      packages=find_packages(),
      package_data={
          '': ['*.svg', '*.js', '*.html', '*.css', '*.png', '*.ico']
      },
      install_requires=[
          'six',
          'gevent',
          'werkzeug',
          'json5',
      ],
      entry_points={
          'console_scripts': [
              'rws=cmsranking.RankingWebServer:main',
          ]
      })
