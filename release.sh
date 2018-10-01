#!/bin/bash

git checkout master
git pull

# Update version in project
PYVAR="__version__ = "
VERSION_STRING=`date -u +0.%Y.%m.%d.%H%M`
FILE_NAME='__init__.py'

# Update ipwb version
echo $PYVAR\'$VERSION_STRING\'>'ipwb/'$FILE_NAME

# Push to GitHub
git add 'ipwb/'$FILE_NAME
git commit -m "RELEASE: Bump version to "$VERSION_STRING

# Create a tag in repo
TAG_NAME='v'$VERSION_STRING
git tag $TAG_NAME
git push
git push origin $TAG_NAME

# Install release requirements for pypi push
pip install twine

# Push to pypi
rm -rf dist; python setup.py sdist bdist_wheel; twine upload dist/*
