[![travis build](https://img.shields.io/travis/jvrana/magicdir.svg)](https://travis-ci.org/jvrana/magicdir)
[![Coverage Status](https://coveralls.io/repos/github/jvrana/magicdir/badge.svg?branch=master)](https://coveralls.io/github/jvrana/magicdir?branch=master)
[![PyPI version](https://badge.fury.io/py/REPO.svg)](https://badge.fury.io/py/REPO)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![module_icon](images/module_icon.png?raw=true)

#### Build/Coverage Status
Branch | Build | Coverage
:---: | :---: | :---:
**master** | [![travis build](https://img.shields.io/travis/jvrana/magicdir/master.svg)](https://travis-ci.org/jvrana/magicdir/master) | [![Coverage Status](https://coveralls.io/repos/github/jvrana/magicdir/badge.svg?branch=master)](https://coveralls.io/github/jvrana/magicdir?branch=master)
**development** | [![travis build](https://img.shields.io/travis/jvrana/magicdir/development.svg)](https://travis-ci.org/jvrana/magicdir/development) | [![Coverage Status](https://coveralls.io/repos/github/jvrana/magicdir/badge.svg?branch=development)](https://coveralls.io/github/jvrana/magicdir?branch=development)

# MagicDir

Dealing with paths and directories isn't rocket science, but it can be a pain. **MagicDir** allows you to build directory trees by treating
your directory tree as a first-class object.

![live_example](images/magicdir_example.gif?raw=true)

Its very easy to create, move, or delete directory trees. For example, the following builds the directory
skeleton for this repo.

![example](images/directory_example.png?raw=true)

```python
from magicdir import *

# create folder structure
env = MagicDir('magicdir')
env.add('magicdir', alias='core')
env.core.add('tests')
env.tests.add('env')
env.tests.add('env2')

# make the directory
env.set_dir(Path(__file__).absolute().parent)
env.mkdirs()

# write some files
env.write('README.md', 'w', '# Magic Dir\nThis is a test readme file')
env.core.write("__init__.py", "w", "__version__ = \"1.0\"")
```

Other things you can do:

```python


```

# Installation

Installation via pip is the easiest way...

```bash
pip install magicdir
```

# Basic usage

Use `add` to create folders.

```python
from magicdir import *

env = MagicDir('bin')
env.add('subfolder1')
env.add('subfolder2')
env.print()

>>>
*bin
|   *subfolder1
|   *subfolder2
```

Functions return MagicDir objects and so can be chained together.
```python
env = MagicDir('bin')
env.add('subfolder1').add('subsubfolder')
env.print()

>>>
*bin
|   *subfolder1
|   |   *subsubfolder
```

Add can be chained together
```python
env = MagicDir('bin')
env.add('subfolder1').add('subsubfolder')
env.print()

>>>
*bin
|   *subfolder1
|   |   *subsubfolder
```

Folders create accesible MagicDir attributes automatically. Alternative attribute names can be set using
'alias='

```python
env = MagicDir('bin')
env.add('subfolder1')
env.subfolder1.add('misc')
env.subfolder1.misc.add('.hidden', alias='hidden')
env.subfolder1.misc.hidden.add('hiddenbin')
env.print()

*bin
|   *subfolder1
|   |   *misc
|   |   |   *.hidden ("hidden")
|   |   |   |   *hiddenbin

```

By default, attributes are *pushed* back the the root directory. The following is equivalent to above.

```python
env = MagicDir('bin')
env.add('subfolder1')
env.subfolder1.add('misc')
env.misc.add('.hidden', alias='hidden')
env.hidden.add('hiddenbin')
env.print()

*bin
|   *subfolder1
|   |   *misc
|   |   |   *.hidden ("hidden")
|   |   |   |   *hiddenbin

```

# Making, moving, copying, and deleting directories

The location of the root folder can be set by `set_bin`

```python
env.set_bin('../bin')
```

Directories can be created, deleted, copied or moved using `mkdirs`, `cpdirs`, `mvdirs`, `rmdirs`

```python
env.mkdirs()
env_copy = env.cpdirs()
# you can do stuff with env_copy independently
env.mvdirs('~/Document')
env_copy.rmdirs()
```

# Advanced usage

All iterables return special list-like objects that can be chained in one-liners.

```python
env.descendents() # returns a MagicList object

# find all txt files
env.descendents(include_self=True).glob("*.txt")

# recursively change permissions for directories
env.abspaths.chmod(0o444)
```