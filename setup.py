#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Wall setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = ["Click>=7.0"]

# setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="Ben Randerson",
    author_email="ben.m.randerson@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers / Engineers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Pipeline design tools.",
    entry_points={"console_scripts": ["wall=cli:main"]},
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="wall",
    name="wall",
    packages=find_packages(include=["wall"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/benranderson/wall",
    version="0.1.0",
    zip_safe=False,
)
