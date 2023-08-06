#!/usr/bin/env bash

# pi wheel twine setuptools -U

set -ev

rm -rf build
rm -rf dist
python setup.py sdist
python setup.py bdist_egg
python setup.py bdist_wheel
twine upload dist/*
