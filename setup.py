#!/usr/bin/env python
from setuptools import setup, find_packages

with open('Readme.md') as readme:
    long_description = readme.read()

EXCLUDE = [
    'tests',
    'docs',
]

setup(
    name='Hawkeye',
    version='0.1.0a1',
    author='Hisham ElSheshtawy',
    author_email='hisham.elsheshtawy@gmail.com',
    description='A tool for monitoring machines in an intranet',
    long_description=long_description,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Networking :: Monitoring',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='hawkeye networking monitoring command line cli',
    packages=find_packages(exclude=EXCLUDE),
    install_requires=[
        'jsonschema>=2.6.0,<3',
        'paramiko>=2.2.1,<3',
        'psutil>=5.2.2,<6',
        'psycopg2>=2.7.1, <3',
        'pycrypto>=2.6.1,<3',
        'xmltodict>=0.11.0'
    ],
    python_requires='>=3'
)
