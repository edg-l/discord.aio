#!/usr/bin/env sh

# Script made to publish the package to https://pypi.python.org/pypi/discord.aio
pip install --upgrade setuptools wheel

# Go to script directory
cd `(dirname $0)`

# Cleanup
rm -rf dist/
rm -rf build/
rm -rf *.egg-info

# Generate files
python setup.py sdist bdist_wheel

# Upload
twine upload dist/*
