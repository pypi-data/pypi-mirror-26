# dumped
[![Coverage Status](https://coveralls.io/repos/github/GoldsteinE/dumped/badge.svg?branch=master)](https://coveralls.io/github/GoldsteinE/dumped?branch=master)

Dumped: easy & lightweight objects persistence. Excellent code coverage, detailed docs and zero external dependencies.

This module provides Dumped superclass.
You can use it to keep some data between program runs.

```python
>>> class Data(Dumped):
...     FIELDS = ['a', 'b']
...     filename = 'data.json'
...
>>> d = Data()
>>> d.a = 2
>>> d2 = Data()
>>> d2.a
2
```


## API

Inherit from Dumped and define your own `filename`. You're ready to go!

```python
>>> import pickle
>>> class Data(Dumped):
...     FIELDS = ['a', 'b'] # If not specified will be everything but DUMPED_KEYWORDS
...     DUMPER = pickle # If not specified will be json. Should provide json-like interface (dump, load)
...     BINARY = True # Need to specify it for opening files to "wb" and "rb" instead of "r" and "w"
...     def __init__(self, id):
...         self.id = id # We will use it for generating filenames
...         # No need to write anything else here, metaclass will do it for you
...     @property
...     def filename(self): # Can be just string if you want class to be singleton
...         return 'data-{}.pickle'.format(self.id)
...
>>> d1 = Data(1)
>>> d2 = Data(2)
>>> d1.a
>>> d1.a = 2
>>> d1.a
2
>>> d2.a
>>> d2.b = 3
>>> d1.b
>>> d2.b
3
>>> del d2.b
>>> d2.b
>>> d1.c
Traceback (most recent call last):
    ...
AttributeError: 'Data' object has no attribute 'c'
```

### Contributing
This repo is open for pull requests!
Before you commit, run tests, check code coverage and documentation. All code should be PEP8-compiant with only except of E501: line length can be up to 120 characters.
