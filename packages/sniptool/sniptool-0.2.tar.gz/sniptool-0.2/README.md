# sniptool by Richard Cook

Code snippet management tool

## Clone repository

```
git clone https://github.com/rcook/sniptool.git
```

## Set up Python virtual environment

```
script/virtualenv
```

## Run main script in virtual environment

```
script/env sniptool version
```

## Dev-install main script in virtual environment

```
script\env pip install -e .
```

This will allow edits to the scripts to be picked up automatically

## Build package

```
script/env python setup.py build
```

## Test package

```
script/env python setup.py test
```

## Upload package

```
script/env python setup.py sdist upload
```

## Install package into global site packages

```
python setup.py install --record files.txt
```

Note that this calls the `python` global Python instead of the Python in the project's virtual environment.

## Licence

Released under [MIT License][licence]

[licence]: LICENSE
