# sniptool by Richard Cook

Code snippet management tool

## Clone repository

```
git clone https://github.com/rcook/sniptool.git
```

## Create Python virtual environment

```
script/virtualenv
```

## Run main script

```
script/sniptool
```

## Build package

```
script/setup build
```

## Test package

```
script/setup test
```

## Upload package

```
script/setup sdist upload
```

## Install package locally

```
python setup.py install --record files.txt
```

Note that this calls the `python` global Python instead of the Python in the project's virtual environment.

## Licence

Released under [MIT License][licence]

[licence]: LICENSE
