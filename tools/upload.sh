#!/usr/bin/env bash
python setup.py sdist bdist_wheel && python3 -m twine upload dist/*
rm -r build
rm -r dist
rm -r ev3db.egg-info