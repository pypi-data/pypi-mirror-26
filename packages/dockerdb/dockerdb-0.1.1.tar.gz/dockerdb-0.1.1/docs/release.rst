How to release
==============

rm -rf dist
python setup.py sdist
twine upload sdist/*
