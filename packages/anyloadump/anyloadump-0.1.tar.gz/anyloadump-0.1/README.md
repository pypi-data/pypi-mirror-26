# Anyloadump

[![Build Status](https://travis-ci.org/knknkn1162/anyloadump.svg?branch=master)](https://travis-ci.org/knknkn1162/anyloadump)
[![Coverage Status](https://coveralls.io/repos/github/knknkn1162/anyloadump/badge.svg?branch=master)](https://coveralls.io/github/knknkn1162/anyloadump?branch=master)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

The Python library anyloadump helps to load a file or to dump to a file briefly in various file formats (e.g. json, pickle, yaml, toml..) with importing modules dynamically.

## Motivation

If the multiple types of file are loaded or dumped, boilerplate code will be generated and scattered as follows:

```python
# import each module.
import json, pickle
with open(json_file, "r") as f:
  json_obj = json.load(f)
  
## do something useful
  
# almost the same as above! Some feel this annoying.
with open(pickle_file, "rb") as f:
  pickle_obj = pickle.load(f)
```

This code goes against DRY(Don't repeat yourself) principle. Let's apply DRY in the problem.

 ```python
 # import json, pickle,... <= unnecessary expression because of dynamic importing
 # what we want to do
 def generalized_load(file):
  with open(file, get_mode()) as fp:
    obj = get_module().load(fp)
    
 # or dump version
 def generalized_dump(obj, file):
  with open(file, get_mode()) as fp:
    get_module().dump(obj, fp)
 ```
 
Anyloadump helps to load a file or to dump to a file briefly in various file types, and provides dump/load/dumps/loads method like [uiri/toml](https://github.com/uiri/toml).

## Installation

To install the latest release on PyPi, simply run:

```python
pip install anyloadump
```

## Tutorial

Here is quick tutorial and is so easy to use:)

```python
import anyloadump as ald

json_file = "sample.json"
obj = ald.load(json_file)

# binary file can be also loaded properly. 
pickle_file = "sample.pickle"
obj = ald.load(pickle_file)

# use library from PyPI. `pip install pyyaml` in advance.
yaml_file = "sample.yaml"
obj = ald.load(yaml_file)

# set encoding option in open method
pickle_file = "sample.pickle"
obj = ald.load(pickle_file, encoding="utf-8")

# set default_flow_style=False, allow_unicode=True in yaml
yaml_file = "sample.yaml"
obj = ald.load(yaml_file, default_flow_style=False, allow_unicode=True)

# ---

obj = get_obj()
# Of course, you can use dump method likewise:
json_file = "sample.json"
ald.dump(obj, json_file)

# binary file can be also loaded properly. 
pickle_file = "sample.pickle"
ald.dump(obj, pickle_file)

# when use loads/dumps, fmt argument is required
ald.dumps(obj, fmt="json")
```

## Requirements

Anyloadump makes use of the art of duck typing to modules, and the imported module meets a few requirements and options:

1. `load(fp, **kwargs)` # fp : file object.
2. `dump(obj, fp, **kwargs)` # obj : Python object, fp : file object
3. (Optional) `loads(s, **kwargs)` # serialized bytes or strs
4. (Optional) `dumps(obj, **kwargs)` # obj : Python object

Note)
1. argument names (obj, fp) are arbitrary.
2. kwargs are the keyword arguments that are optional arguments of load/dump/loads/dumps method.

Check it out that `json, pickle, toml` modules have 1\~4 respectively, by contrast `pyyaml` library only 1\~2.
If you run `anyloadump.loads("sample.yaml")`, CharsetNotInferredError is raised. 



## Note
 
+ Anyloadump imports module dynamically with `importlib.import_module` method. So if you want to use external library such as [yaml/pyyaml](https://github.com/yaml/pyyaml) or [uiri/toml](https://github.com/uiri/toml), run `pip install` in advance. Or raise ImportError/ModuleNotFoundError(new in Python3.6).
