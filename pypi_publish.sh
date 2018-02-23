#!/usr/bin/env sh

# Script made to publish the package to https://pypi.org/project/discord.py/

cd `(dirname $0)`
rm -rf dist/
rm -rf *.aio.egg-info
python3 setup.py sdist
python3 setup.py bdist
gpg --detach-sign -a dist/*.tar.gz
twine upload dist/*