# sklearn-features

[![Build Status](https://travis-ci.org/sixtwoeight-tech/sklearn-features.svg?branch=master)](https://travis-ci.org/sixtwoeight-tech/sklearn-features) [![Docs Status](https://readthedocs.org/projects/sklearn-features/badge/?version=latest)](http://sklearn-features.readthedocs.io/en/latest/?badge=latest)


## Tests

In the root directory run

```
ptest --pyargs src
```


## Build

```
rm -rf dist/
python setup.py sdist
python setup.py bdist_wheel
```

## Release

```
twine upload dist/*
```
