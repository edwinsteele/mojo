#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', "requests", "anycache"]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Edwin Steele",
    author_email='edwin@wordspeak.org',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Mojo analyses power usage data from MojoEnergy",
    entry_points={
        'console_scripts': [
            'mojo=mojo.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='mojo',
    name='mojo',
    packages=find_packages(include=['mojo']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/edwinsteele/mojo',
    version='0.1.0',
    zip_safe=False,
)
