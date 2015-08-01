**Alpha Warning! Until `1.0.0`, `progressive` will likely be going under some kind of radical API revision every minor release; just a forewarning.**

# `progressive`

[![Build Status](https://travis-ci.org/hfaran/progressive.svg?branch=master)](https://travis-ci.org/hfaran/progressive?branch=master)
[![Coverage Status](https://coveralls.io/repos/hfaran/progressive/badge.svg?branch=master)](https://coveralls.io/r/hfaran/progressive?branch=master)
[![PyPI version](https://badge.fury.io/py/progressive.svg)](http://badge.fury.io/py/progressive)
[![Documentation Status](https://readthedocs.org/projects/progressive/badge/?version=latest)](https://readthedocs.org/projects/progressive/?badge=latest)
[![Stories in Ready](https://badge.waffle.io/hfaran/progressive.png?label=Ready)](http://waffle.io/hfaran/progressive)

Colorful progress bars and trees for your terminal, powered by [blessings](https://github.com/erikrose/blessings). Compatible with both Python 2 and 3.

## Introduction

`progressive` lets you view progress of complex workflows as well as simple ones:

[![Tree Progress View](https://raw.githubusercontent.com/hfaran/progressive/master/example.gif)](https://github.com/hfaran/progressive)


## Installation

* For the possibly stable

```
pip install progressive
```

* For the latest and greatest

```
git clone https://github.com/hfaran/progressive.git
cd progressive
python setup.py install
```

## Getting Started

* There is preliminary documentation is available at [readthedocs](http://progressive.readthedocs.org/) but more detailed documentation is coming soon on completion of the 1.0 API, but in the meantime check out the [examples](https://github.com/hfaran/progressive/blob/master/progressive/examples.py).
* `progressive` supports graceful fallback modes for terminals without colors, [but you really should upgrade your terminal to 256 colors](http://pastelinux.wordpress.com/2010/12/01/upgrading-linux-terminal-to-256-colors/) to make full use of `progressive`.
