#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='python-git-info',
    version='0.1.0',
    description='Get git information repository, directly from .git',

    author='Serafeim Papastefanos',
    author_email='spapas@gmail.com',
    license='MIT',
    url='https://github.com/spapas/python-git-info/',
    zip_safe=False,
    include_package_data=False,
    packages=find_packages(exclude=['tests.*', 'tests', 'sample', ]),

    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
