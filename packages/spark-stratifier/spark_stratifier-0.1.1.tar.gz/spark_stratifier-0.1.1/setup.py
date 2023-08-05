#!/usr/bin/env python

from setuptools import setup

version = '0.1.1'

setup(
    name='spark_stratifier',
    version=version,
    description='Stratified Cross Validator for Spark',
    author='Justin Suen',
    author_email='justin.suen@hackerrank.com',
    url='https://github.com/interviewstreet/spark-stratifier',
    license='MIT',
    packages=['spark_stratifier'],
    install_requires=open('./requirements.txt').read().split()
)
