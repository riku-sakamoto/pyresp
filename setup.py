# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md',encoding="utf-8") as f:
  readme = f.read()

with open('LICENSE',encoding="utf-8") as f:
	license = f.read()

setup(
	name='pyresp',
	version='0.1.0',
	description='Python Libraries for RESP Output Files',
	long_description=readme,
	author='Riku Sakamoto',
	author_email='riku-sakamoto@kke.co.jp',
	url='https://github.com/riku-sakamoto/pyresp',
	license=license,
	packages=find_packages(exclude=('tests', 'docs','RESPToolKitEnv'))
)

