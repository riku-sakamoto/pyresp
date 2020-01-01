# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
  readme = f.read()

with open('LICENSE') as f:
	license = f.read()

setup(
	name='pyresp',
	version='0.1.0',
	description='Python Libraries for RESP output files',
	long_description=readme,
	author='Riku Sakamoto',
	author_email='riku-sakamoto@kke.co.jp',
	url='https://github.com/riku-sakamoto/pyresp',
	license=license,
	packages=find_packages(exclude=('tests', 'docs','RESPToolKitEnv'))
)

